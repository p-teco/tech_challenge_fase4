import argparse
import json
from itertools import islice
from pathlib import Path
from time import perf_counter
from urllib.request import Request, urlopen

import chromadb


MODELO = "embeddinggemma-2:270m"


def gerar_embeddings(textos):
    dados = json.dumps({"model": MODELO, "input": textos, "truncate": False}).encode("utf-8")
    requisicao = Request("http://127.0.0.1:11434/api/embed", data=dados, headers={"Content-Type": "application/json"})
    with urlopen(requisicao, timeout=180) as resposta:
        vetores = json.load(resposta)["embeddings"]
    if len(vetores) != len(textos) or any(not vetor for vetor in vetores):
        raise ValueError("O Ollama não retornou um vetor para cada texto.")
    return vetores


def indexar(origem, destino, limite):
    if limite <= 0:
        raise ValueError("O limite deve ser maior que zero.")
    if destino.exists():
        raise FileExistsError(f"O diretório de destino já existe: {destino}")

    with origem.open(encoding="utf-8") as arquivo:
        documentos = [json.loads(linha) for linha in islice(arquivo, limite)]
    if not documentos:
        raise ValueError("O arquivo não contém documentos para indexar.")

    inicio = perf_counter()
    banco = chromadb.PersistentClient(path=str(destino))
    colecao = banco.create_collection(
        name="avaliacoes", embedding_function=None,
        configuration={"hnsw": {"space": "cosine"}}, metadata={"modelo": MODELO},
    )
    for inicio_lote in range(0, len(documentos), 10):
        lote = documentos[inicio_lote:inicio_lote + 10]
        vetores = gerar_embeddings([f"title: none | text: {documento['texto']}" for documento in lote])
        colecao.add(
            ids=[f"{documento['review_id']}:{documento['order_id']}" for documento in lote],
            embeddings=vetores,
            documents=[documento["texto"] for documento in lote],
            metadatas=[{campo: documento[campo] for campo in ("review_id", "order_id", "review_score")} for documento in lote],
        )
        print(f"Indexados: {colecao.count()}/{len(documentos)}", flush=True)
    print(f"Tempo de indexação: {perf_counter() - inicio:.1f} segundos")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Indexa avaliações no Chroma local.")
    parser.add_argument("origem", type=Path, help="Arquivo JSONL preparado")
    parser.add_argument("destino", type=Path, help="Novo diretório para o banco")
    parser.add_argument("--limite", type=int, required=True, help="Quantidade máxima de avaliações")
    argumentos = parser.parse_args()
    indexar(argumentos.origem, argumentos.destino, argumentos.limite)
