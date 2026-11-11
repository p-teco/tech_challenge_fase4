# Voice of Customer Intelligence

Projeto de análise de avaliações de clientes da Olist com recuperação de informações e geração de respostas fundamentadas em evidências.

## Estrutura

- `scripts/`: scripts para exploração da base de dados.

## Exploração das avaliações

Com Python 3 instalado, execute o comando abaixo informando o caminho para o arquivo de avaliações da base Olist:

```powershell
python scripts/explorar_avaliacoes.py caminho/olist_order_reviews_dataset.csv
```

O script apresenta a quantidade de registros, o preenchimento dos campos, a presença e o tamanho dos textos, a distribuição das notas e a repetição de identificadores. Ele utiliza apenas bibliotecas da instalação padrão do Python e não altera a base.

Para a construção da base de conhecimento, serão consideradas inicialmente as avaliações com título ou mensagem. Cada avaliação será tratada como um documento, preservando `review_id` e `order_id` para rastrear as evidências. Foram identificado valores de `review_id` repetidos, enquanto a combinação dos dois campos é única nos registros selecionados.

Avaliações sem título e sem mensagem ficam fora da base textual porque a nota, isoladamente, não explica os motivos de satisfação ou insatisfação. Elas podem contribuir para análises quantitativas, mas não fornecem relatos para fundamentar as respostas do RAG.
