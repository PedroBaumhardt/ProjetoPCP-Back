import datetime
import math
import uuid
from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.model import OrdemProducaoModel
from app.core.repository import OrdemProducaoRepository
from app.core.service import BaseService
from app.core.service.ProductService import ProductService
from app.core.service.ProductStructureService import ProductStructureService
from app.core.service.StockService import StockService

_MINUTES_PER_DAY = 24 * 60

class ProductionOrderService(BaseService[OrdemProducaoModel]):
    repository: OrdemProducaoRepository

    _STATUS: dict[str, str] = {
        "ready": "liberada",
        "in_progress": "em_producao",
        "finished": "concluida",
        "cancelled": "cancelada",
    }
    _INITIAL_STATUS: str = _STATUS["ready"]
    _OUTSIDE_SEQUENCE: int = -1

    def __init__(self, session: AsyncSession):
        super().__init__(OrdemProducaoRepository(session))

    async def get_all(self) -> list[dict]:
        data = await self.repository.get_all()
        dict_data = []
        for item in data:
            dict_data.append(item.to_dict())
        return dict_data

    async def get_by_id(self, id: str) -> dict:
        data = await self.repository.get_by_id(uuid.UUID(id))
        if not data:
            raise ValueError("Production order not found")
        return data.to_dict()

    async def update_priority(self, id: str, priority: str) -> None:
        mdl = await self.repository.get_by_id(uuid.UUID(id))
        if not mdl:
            raise ValueError("Production order not found")
        mdl.prioridade = priority
        await self.repository.update(mdl)

    async def create(self,
                     numero: str,
                     produto_codigo: str,
                     prioridade: str,
                     quantidade_planejada: int,
                     data_inicio_prevista: datetime.date,
                     data_emissao: datetime.date | None = None,
                     pedido_numero: str | None = None,
                     observacao: str | None = None,
                     ) -> None:
        if data_emissao is None:
            data_emissao = datetime.date.today()

        sequencia_programacao = await self.repository.get_highest_sequencia_programacao()
        if sequencia_programacao is None:
            sequencia_programacao = -1
        sequencia_programacao += 1

        production_days = await self._get_prod_time_by_code_in_days(produto_codigo,
                                                                    ProductService(self.repository.session),
                                                                    mult=quantidade_planejada)

        current_highest_date = await self.repository.get_higher_data_fim_prevista()
        if not current_highest_date or current_highest_date < data_inicio_prevista:
            current_highest_date = data_inicio_prevista
        data_fim_prevista = current_highest_date + datetime.timedelta(days=production_days)

        status = self._INITIAL_STATUS
        quantidade_produzida = 0

        mdl = OrdemProducaoModel(
            numero=numero,
            produto_codigo=produto_codigo,
            pedido_numero=pedido_numero,
            prioridade=prioridade,
            sequencia_programacao=sequencia_programacao,
            quantidade_planejada=quantidade_planejada,
            quantidade_produzida=quantidade_produzida,
            data_emissao=data_emissao,
            data_inicio_prevista=data_inicio_prevista,
            data_fim_prevista=data_fim_prevista,
            status=status,
            observacao=observacao
        )
        await self.repository.create(mdl)

    async def start(self, id: str) -> None:
        id = uuid.UUID(id)
        mdl = await self.repository.get_by_id(id)

        if not mdl:
            raise ValueError("Production order not found")
        elif mdl.status != self._STATUS["ready"]:
            raise ValueError("Production order is not in a valis state to start")

        p_structure_service = ProductStructureService(self.repository.session)
        materials = await p_structure_service.get_material_quantities_with_product_code(mdl.produto_codigo)

        stock_service = StockService(self.repository.session)
        for material, qty_per_unit in materials.items():
            await stock_service.reserve_by_material_code(material, qty_per_unit * mdl.quantidade_planejada)

        mdl.status = self._STATUS["in_progress"]
        await self.repository.update(mdl)

    async def cancel(self, id: str) -> None:
        id = uuid.UUID(id)
        mdl = await self.repository.get_by_id(id)

        if not mdl:
            raise ValueError("Production order not found")
        elif mdl.status == self._STATUS["finished"]:
            raise ValueError("Production order already finished")

        mdl.status = self._STATUS["cancelled"]
        location = await self._remove_from_sequence(mdl)

        await self._recalc_ending_date_since(location)

    async def produce(self, id: str) -> int: # Produz 1 unidade e retorna a quantidade produzida até agora
        id = uuid.UUID(id)

        mdl = await self.repository.get_by_id(id)
        if mdl is None:
            raise ValueError("Production order not found")
        elif mdl.status != self._STATUS["in_progress"]:
            raise ValueError("Production order is not in progress")
        elif mdl.quantidade_produzida >= mdl.quantidade_planejada:
            raise ValueError("Production order already reached its planned quantity")

        # Consome da reserva feita no start a quantidade de cada material para 1 unidade do produto
        p_structure_service = ProductStructureService(self.repository.session)
        materials = await p_structure_service.get_material_quantities_with_product_code(mdl.produto_codigo)

        stock_service = StockService(self.repository.session)
        for material, qty_per_unit in materials.items():
            await stock_service.consume_reserved_by_material_code(material, qty_per_unit)

        mdl.quantidade_produzida += 1
        await self.repository.update(mdl)

        if mdl.quantidade_produzida >= mdl.quantidade_planejada:
            await self.end(mdl)

        return mdl.quantidade_produzida

    async def end(self, mdl: OrdemProducaoModel) -> None:
        pass

    async def update_sequence_number(self, id: str, new_seq_number: int) -> None:
        # Regras: Se novo numero já está na fila, trocam de lugar
        #         Se novo numero é maior que fim da fila, vai para o fim da fila
        id = uuid.UUID(id)

        if new_seq_number < 0:
            raise ValueError("Sequence number can't be negative")

        mdl = await self.repository.get_by_id(id)
        if mdl is None:
            raise ValueError("Production order not found")
        elif mdl.status != self._STATUS["ready"]:
            raise ValueError("Production order is not in a valid state to change sequence")
        elif mdl.sequencia_programacao < 0:
            raise ValueError("Production order is not in the sequence")

        mdl_at_location = await self.repository.get_by_sequence_num(new_seq_number)
        if mdl_at_location is not None:
            await self._flip_sequence_numbers(mdl, mdl_at_location)
            return

        # Ainda contém a própria mdl, então nunca é None aqui. Após a remoção abaixo, essa posição fica livre
        end_of_queue = await self.repository.get_highest_sequencia_programacao()
        end_of_queue = cast(int, end_of_queue)

        location = await self._remove_from_sequence(mdl)
        mdl.sequencia_programacao = end_of_queue
        await self.repository.update(mdl)

        await self._recalc_ending_date_since(location)

    async def _flip_sequence_numbers(self, mdl1: OrdemProducaoModel, mdl2: OrdemProducaoModel) -> None:
        seq1, seq2 = mdl1.sequencia_programacao, mdl2.sequencia_programacao
        if seq1 == seq2:
            return

        # O índice único não é adiável: tira mdl1 da fila antes de trocar, gravando a cada passo
        mdl1.sequencia_programacao = self._OUTSIDE_SEQUENCE
        await self.repository.update(mdl1)

        mdl2.sequencia_programacao = seq1
        await self.repository.update(mdl2)

        mdl1.sequencia_programacao = seq2
        await self.repository.update(mdl1)

        await self._recalc_ending_date_since(min(seq1, seq2))

    @staticmethod
    async def _get_prod_time_by_code_in_days(cod: str, prod_service: ProductService, mult: int = 1) -> int:
        production_minutes = await prod_service.get_production_time_by_code(cod)
        production_minutes *= mult
        production_days = math.ceil(production_minutes / _MINUTES_PER_DAY)
        return production_days

    async def _remove_from_sequence(self, mdl: OrdemProducaoModel) -> int: # Retorna o local onde foi removido da sequencia
        starting_point = mdl.sequencia_programacao

        mdl.sequencia_programacao = self._OUTSIDE_SEQUENCE
        await self.repository.update(mdl)

        mdl_list = await self.repository.get_all_sequence_ordered(starting_point)
        for mdl in mdl_list:
            mdl.sequencia_programacao -= 1
            await self.repository.update(mdl)
        return starting_point

    async def _recalc_ending_date_since(self, since:int = 0) -> None:
        product_service = ProductService(self.repository.session)

        since_query = since
        if since < 0:
            raise KeyError("Cant calc dates with negative sequence")
        elif since > 0:
            since_query -= 1 # Faz a query buscando 1 anterior para usar de ponto de partida nos calculos

        mdl_list = await self.repository.get_all_sequence_ordered(since=since_query)
        if len(mdl_list) <= 0:
            return

        # Se vamos recalcular tudo, não tem uma data de partida
        curr_high_dt = mdl_list[0].data_fim_prevista if since > 0 else datetime.date.today()
        for mdl in mdl_list:
            if mdl.sequencia_programacao < since: continue

            # Mesma regra do create: começa no fim da fila ou na data pedida pelo cliente, o que for maior
            start_dt = max(curr_high_dt, mdl.data_inicio_prevista)
            production_time = await self._get_prod_time_by_code_in_days(mdl.produto_codigo,
                                                                         product_service,
                                                                         mult=mdl.quantidade_planejada)
            mdl.data_fim_prevista = start_dt + datetime.timedelta(days=production_time)
            curr_high_dt = mdl.data_fim_prevista

            await self.repository.update(mdl)