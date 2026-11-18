# Contexto do Projeto — FastAPI PCP

## Visão Geral

API REST em FastAPI para gestão de PCP (Planejamento e Controle de Produção). Usa async SQLAlchemy com PostgreSQL e Alembic para migrations.

## Arquitetura

Fluxo: **Router → Controller → Service → Repository → Model**

- Até Service é considerado **domínio**
- Controllers e Services de domínio são agrupados por funcionalidade (ex: `ImportController`, `ImportService`), não um por entidade
- Existem `BaseController`, `BaseService` e `BaseRepository` genéricos (com CRUD) para uso futuro

```
app/
├── cmd/api/              -- entrypoint e lifespan da aplicação
├── core/
│   ├── config/           -- Settings, database (async engine/session)
│   ├── controller/       -- BaseController + controllers de domínio (ImportController)
│   ├── http/
│   │   ├── Router.py     -- registro de rotas
│   │   ├── dependencies.py -- SessionDep (injeção de sessão async)
│   │   └── routes/       -- arquivos de rota (import.py, example.py)
│   ├── model/            -- SQLAlchemy models (BaseModel + 11 entidades)
│   ├── repository/       -- BaseRepository + 11 repositories concretos
│   └── service/          -- BaseService + services de domínio (ImportService)
└── util/
```

## Models (11 entidades)

### Tabelas base (sem FK entre si)
- **RecursoModel** — recursos produtivos (máquinas, mão de obra)
- **MaterialModel** — matérias-primas e insumos
- **ClienteModel** — clientes (nome, email, telefone)
- **ProdutoModel** — produtos acabados

### Tabelas com dependência simples
- **EstoqueModel** — estoque por material (FK: material_codigo)

### Pivots / Cabeçalhos (1:1 com Produto)
- **RoteiroModel** — cabeçalho do roteiro (1:1 com Produto via unique)
- **EstruturaProdutoModel** — cabeçalho da estrutura (1:1 com Produto via unique)

### Sub-tabelas (1:N com pivot)
- **PassoRoteiroModel** — passos do roteiro (FK: roteiro_id, recurso_codigo)
- **ComponenteModel** — componentes da estrutura (FK: estrutura_id, material_codigo)

### Tabelas de negócio
- **PedidoModel** — pedidos de venda (FK: cliente_id, produto_codigo)
- **OrdemProducaoModel** — ordens de produção (FK: produto_codigo, pedido_numero opcional)

## Padrões de Código

- Comentários usam `# --` (não parecer IA)
- Models herdam de `BaseModel` que define `id` (UUID), `created_at`, `updated_at`
- Repositories são genéricos: `BaseRepository[T]` com `get_all`, `get_by_id`, `create`, `update`, `delete`
- CSV import usa delimitador `;`, encoding UTF-8-sig
- Toda a lógica de domínio (parsing, resolução de FKs) fica no Service, não no Controller ou na Rota

## Importação CSV

Ordem de importação documentada em `observations.md` (gitignored). Resumo:
1. Recurso, Material, Cliente, Produto (sem dependências, qualquer ordem)
2. Estoque, Roteiro, EstruturaProduto (dependem das bases)
3. PassoRoteiro, Componente (dependem dos pivots)
4. Pedido (depende de Cliente + Produto)
5. OrdemProducao (depende de Produto + Pedido opcional)

## Arquivos Importantes

- `observations.md` — ordem de importação (gitignored)
- `alembic/` — migrations
- `pyproject.toml` — dependências (uv)
