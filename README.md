# Trabalho Prático: Implementação de Testes de Software

Suíte de testes automatizados (Unitários, de Componente e de Integração) para a aplicação de Controle de Gastos Familiares, cobrindo as classes `Categoria`, `FormaPagamento`, `Pessoa` e `Movimento`.

## Como instalar as dependências

Com o Python 3.10+ instalado, a partir da raiz do projeto:

```bash
pip install -r requirements.txt
```

## Como rodar a suíte completa de testes

A partir da raiz do projeto:

```bash
python -m pytest
```

Para ver o nome de cada teste individualmente (modo verboso):

```bash
python -m pytest -v
```

Para rodar os testes de uma entidade específica:

```bash
python -m pytest tests/test_categoria.py -v
python -m pytest tests/test_forma_pagamento.py -v
python -m pytest tests/test_pessoa.py -v
python -m pytest tests/test_movimento.py -v
```

## Estrutura dos testes

Cada arquivo em `tests/` segue a mesma organização, dividida em três camadas:

- **Testes Unitários** — validam a classe de domínio isolada (criação, getters/setters, validação de dados como formato de data, serialização `to_dict`/`from_dict`), sem tocar em arquivos ou depender de outras classes.
- **Testes de Componente** — validam o CRUD completo (criar, listar, atualizar, remover) de cada entidade acoplada ao `RepositorioCSV`, usando um diretório temporário isolado por teste (via fixture `pytest`), sem afetar arquivos reais do projeto.
- **Testes de Integração** — validam regras de negócio que cruzam múltiplas classes, como o bloqueio de remoção de uma `Categoria`/`FormaPagamento`/`Pessoa` quando há um `Movimento` atrelado, e o fluxo completo de registrar um movimento associando `Pessoa`, `Categoria` e `FormaPagamento`.

## Observação sobre o código-base

Durante o desenvolvimento dos testes de Componente, foi identificado e corrigido um bug em `model/repositorio.py`: os métodos `atualizar` e `remover` comparavam `row["id"]` com a função embutida `id()` do Python (por sombreamento de nome), em vez de compará-la com o parâmetro `id` recebido — o que fazia essas operações nunca encontrarem a linha correta no CSV. A correção foi validada pelos testes `test_atualizar` e `test_remover` de cada entidade.