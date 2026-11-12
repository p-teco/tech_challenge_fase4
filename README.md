# Voice of Customer Intelligence

Projeto de análise de avaliações de clientes da Olist com recuperação de informações e geração de respostas fundamentadas em evidências.

## Banco vetorial

O Chroma foi escolhido para armazenar localmente os vetores, os comentários e seus metadados, permitindo recuperar as evidências sem configurar um servidor separado.

## Estrutura

- `scripts/`: scripts para exploração, preparação e busca das avaliações.
- `avaliacao/`: exemplos para avaliar as respostas geradas.

## Exploração das avaliações

Com Python 3 instalado, execute o comando abaixo informando o caminho para o arquivo de avaliações da base Olist:

```powershell
python scripts/explorar_avaliacoes.py caminho/olist_order_reviews_dataset.csv
```

O script apresenta a quantidade de registros, o preenchimento dos campos, a presença e o tamanho dos textos, a distribuição das notas e a repetição de identificadores. Ele utiliza apenas bibliotecas da instalação padrão do Python e não altera a base.

Na base de conhecimento, cada avaliação com título ou mensagem é tratada como um documento. Os campos `review_id` e `order_id` identificam a avaliação e permitem rastrear as evidências. Alguns valores de `review_id` se repetem, mas a combinação dos dois campos é única nos registros selecionados.

Avaliações sem título e sem mensagem ficam fora da base textual porque a nota, isoladamente, não explica os motivos de satisfação ou insatisfação. Elas podem contribuir para análises quantitativas, mas não fornecem relatos para fundamentar as respostas do RAG.

## Preparação das avaliações

Para gerar um arquivo JSONL com as avaliações selecionadas, execute:

```powershell
python scripts/preparar_avaliacoes.py caminho/olist_order_reviews_dataset.csv data/avaliacoes.jsonl
```

Cada linha contém os identificadores da avaliação e do pedido, a nota e o texto formado pelo título e pela mensagem disponíveis. O script interrompe a preparação se faltar um identificador, se um par se repetir ou se a nota for inválida.

A nota pode ajudar a contextualizar comentários ambíguos, inclusive quando parecem positivos apesar de uma avaliação baixa. Ainda assim, ela não comprova ironia nem explica, por si só, o motivo da satisfação ou insatisfação.

## Indexação e busca local

Instale o [Ollama para Windows](https://docs.ollama.com/windows), inicie o aplicativo e baixe o modelo usado para gerar embeddings:

```powershell
ollama pull embeddinggemma-2:270m
```

Com o Ollama em execução, crie um ambiente virtual e instale as dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Para indexar as avaliações preparadas e conferir os identificadores no banco:

```powershell
.\.venv\Scripts\python.exe scripts/indexar_avaliacoes.py data/avaliacoes.jsonl data/chroma_completo --limite 42687
.\.venv\Scripts\python.exe scripts/verificar_indice.py data/avaliacoes.jsonl data/chroma_completo
.\.venv\Scripts\python.exe scripts/buscar_avaliacoes.py data/chroma_completo "Quais problemas ocorreram na entrega?"
```

## Avaliação

### Modelo de linguagem

O objetivo é verificar se o modelo fundamenta as respostas nas avaliações fornecidas e reconhece situações sem evidências suficientes.

O script abaixo consulta a API da NVIDIA com três situações fictícias: evidência suficiente, evidência insuficiente e pergunta fora do escopo. A variável de ambiente `NVIDIA_API_KEY` deve estar configurada antes da execução.

```powershell
python avaliacao/avaliar_respostas_nvidia.py --modelo nvidia/nemotron-3.5-super-vl-120b-a12b
```

Para avaliar outro modelo disponível na API, informe o identificador com `--modelo`.

Em uma execução com o Nemotron 3.5 Super, as respostas foram:

| Caso | Resposta |
| --- | --- |
| Com evidência | O problema foi um atraso na entrega: o pedido chegou duas semanas atrasado. [A1] |
| Evidência insuficiente | Não é possível responder por que o pedido atrasou com base nas avaliações disponíveis. A avaliação [A1] apenas informa que o pedido chegou duas semanas atrasado, mas não menciona o motivo do atraso. |
| Fora do escopo | Não é possível responder com os dados disponíveis. A avaliação fornecida ([A1]) trata de produto e entrega e não contém informações sobre a cotação do dólar. |

Os resultados são de uma execução com exemplos fictícios e podem variar entre chamadas.

### Fluxo integrado

O objetivo é verificar se a busca recupera avaliações úteis e se a resposta gerada é coerente com os relatos recuperados.

Para avaliar a recuperação e a geração de respostas em conjunto, use o banco indexado e configure a variável `NVIDIA_API_KEY`:

```powershell
.\.venv\Scripts\python.exe scripts/responder.py data/chroma_completo "Quais problemas ocorreram na entrega?"
.\.venv\Scripts\python.exe scripts/responder.py data/chroma_completo "Qual é a cotação do dólar hoje?"
```

A aplicação recupera avaliações no Chroma e envia a pergunta e os comentários recuperados à API da NVIDIA. A resposta é exibida junto das avaliações e seus identificadores. 

### Comparação da recuperação

O comando apresenta os primeiros 50 resultados em grupos de 1 a 10, 11 a 25 e 26 a 50, permitindo comparar a relevância dos comentários recuperados:

```powershell
.\.venv\Scripts\python.exe avaliacao/comparar_recuperacao.py data/chroma_completo "Quais problemas ocorreram na entrega?"
```
