import argparse
from pathlib import Path

import chromadb

from indexar_avaliacoes import MODELO, gerar_embeddings


def buscar(caminho, pergunta):
    if not caminho.is_dir():
        raise FileNotFoundError(f"Banco não encontrado: {caminho}")
    banco = chromadb.PersistentClient(path=str(caminho))
    colecao = banco.get_collection("avaliacoes", embedding_function=None)
    if (colecao.metadata or {}).get("modelo") != MODELO:
        raise ValueError("O modelo da coleção não corresponde ao modelo de busca.")
    vetor = gerar_embeddings([f"task: question answering | query: {pergunta}"])[0]
    resultados = colecao.query(query_embeddings=[vetor], n_results=min(5, colecao.count()), include=["documents", "metadatas", "distances"])
    for texto, metadados, distancia in zip(resultados["documents"][0], resultados["metadatas"][0], resultados["distances"][0]):
        print(f"\nDistância: {distancia:.4f} | Nota: {metadados['review_score']} | review_id: {metadados['review_id']} | order_id: {metadados['order_id']}")
        print(texto)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Busca avaliações no Chroma local.")
    parser.add_argument("banco", type=Path, help="Diretório do banco Chroma")
    parser.add_argument("pergunta", help="Pergunta para a busca semântica")
    argumentos = parser.parse_args()
    buscar(argumentos.banco, argumentos.pergunta)
