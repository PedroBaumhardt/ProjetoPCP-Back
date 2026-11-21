# Contexto do Projeto — FastAPI PCP

## Visão Geral

API REST em FastAPI para gestão de PCP (Planejamento e Controle de Produção). Usa async SQLAlchemy com PostgreSQL e Alembic para migrations.

## Arquitetura

Fluxo: **Router → Controller → Service → Repository → Model**

- Até Service é considerado **domínio**
- Controllers e Services de domínio são agrupados por funcionalidade (ex: `ImportController`, `ImportService`), não um por entidade
- Existem `BaseService` e `BaseRepository` genéricos (com CRUD) para uso futuro
- `BaseController` NÃO tem CRUD: controllers não importam nem recebem Models, apenas delegam ao Service

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
│   ├── schema/           -- schemas Pydantic dos arquivos JSON de importação (ImportSchema)
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

- Nomes de variáveis, funções, constantes, classes e type aliases em **inglês** (ex: `Text255`, `PASSWORD_MAX_BYTES`, `AuthRequest`). Exceção: campos de schema/model que espelham o layout JSON ou colunas do banco mantêm o nome original (ex: `descricao`, `codigo`)
- Comentários usam `# --` (não parecer IA)
- NÃO colocar comentários de cabeçalho no início dos arquivos (ex: `# -- controller de X: faz Y`); o arquivo começa direto nos imports
- Models herdam de `BaseModel` que define `id` (UUID), `created_at`, `updated_at`
- Repositories são genéricos: `BaseRepository[T]` com `get_all`, `get_by_id`, `get_by_field_in`, `create`, `create_many`, `update`, `delete`
- Importação recebe arquivos JSON (raiz = array) validados por schemas Pydantic em `app/core/schema/`
- Toda a lógica de domínio (parsing, resolução de FKs) fica no Service, não no Controller ou na Rota

## Importação JSON

Layout definido no PDF "Layout arquivos PCP": 7 arquivos JSON, um endpoint `POST /import/<arquivo>` (upload) para cada.
Ordem de importação (por dependência):
1. `recursos`, `materiais` (sem dependências)
2. `produtos` (cria Produto + Roteiro + PassoRoteiro; depende de recursos)
3. `estrutura-produtos` (cria EstruturaProduto + Componente; depende de produtos + materiais)
4. `estoque` (depende de materiais)
5. `pedidos` (depende de produtos ativos; Cliente é buscado/criado pelo nome)
6. `ordens-producao` (depende de produtos + pedidos opcionais)

Erros de layout retornam 422; códigos inexistentes, duplicados ou regras de consistência retornam 400.

## Arquivos Importantes

- `alembic/` — migrations
- `pyproject.toml` — dependências (uv)
