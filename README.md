# Voice of Customer Intelligence

Projeto de análise de avaliações de clientes da Olist com recuperação de informações e geração de respostas fundamentadas em evidências.

## Banco vetorial

O Chroma foi escolhido para armazenar localmente os vetores, os comentários e seus metadados, permitindo recuperar as evidências sem configurar um servidor separado.

## Estrutura

- `scripts/`: scripts para exploração, preparação e busca das avaliações.

## Exploração das avaliações

Com Python 3 instalado, execute o comando abaixo informando o caminho para o arquivo de avaliações da base Olist:

```powershell
python scripts/explorar_avaliacoes.py caminho/olist_order_reviews_dataset.csv
```

O script apresenta a quantidade de registros, o preenchimento dos campos, a presença e o tamanho dos textos, a distribuição das notas e a repetição de identificadores. Ele utiliza apenas bibliotecas da instalação padrão do Python e não altera a base.

Para a construção da base de conhecimento, serão consideradas as avaliações com título ou mensagem. Cada avaliação será tratada como um documento, preservando `review_id` e `order_id` para rastrear as evidências. Foram identificados valores de `review_id` repetidos, enquanto a combinação dos dois campos é única nos registros selecionados.

Avaliações sem título e sem mensagem ficam fora da base textual porque a nota, isoladamente, não explica os motivos de satisfação ou insatisfação. Elas podem contribuir para análises quantitativas, mas não fornecem relatos para fundamentar as respostas do RAG.

## Preparação das avaliações

Para gerar um arquivo JSONL com as avaliações selecionadas, execute:

```powershell
python scripts/preparar_avaliacoes.py caminho/olist_order_reviews_dataset.csv data/avaliacoes.jsonl
```

Cada linha contém os identificadores da avaliação e do pedido, a nota e o texto formado pelo título e pela mensagem disponíveis. O script interrompe a preparação se faltar um identificador, se um par se repetir ou se a nota for inválida.

A nota pode ajudar a contextualizar comentários ambíguos, inclusive quando parecem positivos apesar de uma avaliação baixa. Ainda assim, ela não comprova ironia nem explica, por si só o motivo da satisfação ou insatisfação.

## Indexação e busca local

Com o Ollama em execução e o modelo `embeddinggemma-2:270m` instalado, crie um ambiente virtual e instale as dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Para indexar uma amostra de 20 avaliações e consultar os resultados:

```powershell
.\.venv\Scripts\python.exe scripts/indexar_avaliacoes.py data/avaliacoes.jsonl data/chroma_amostra --limite 20
.\.venv\Scripts\python.exe scripts/buscar_avaliacoes.py data/chroma_amostra "Quais problemas ocorreram na entrega?"
```

