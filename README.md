# Voice of Customer Intelligence

Projeto de análise de avaliações de clientes da Olist com recuperação de informações e geração de respostas fundamentadas em evidências.

## Estrutura

- `scripts/`: scripts para exploração da base de dados.

## Exploração das avaliações

Com Python 3 instalado, execute o comando abaixo informando o caminho para o arquivo de avaliações da base Olist:

```powershell
python scripts/explorar_avaliacoes.py caminho/olist_order_reviews_dataset.csv
```

O script apresenta a quantidade de registros, o preenchimento dos campos e a distribuição das notas. Ele utiliza apenas bibliotecas da instalação padrão do Python e não altera a base.
