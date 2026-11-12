import argparse
import json
import sys
from pathlib import Path

import chromadb


def verificar(origem, banco):
    if not banco.is_dir():
        raise FileNotFoundError(f"Banco não encontrado: {banco}")
    with origem.open(encoding="utf-8") as arquivo:
        documentos = [json.loads(linha) for linha in arquivo]
    ids = [f"{documento['review_id']}:{documento['order_id']}" for documento in documentos]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError("O arquivo preparado está vazio ou possui identificadores repetidos.")

    cliente = chromadb.PersistentClient(path=str(banco))
    colecao = cliente.get_collection("avaliacoes", embedding_function=None)
    indexados = set(colecao.get(include=[])["ids"])
    esperados = set(ids)
    faltantes = len(esperados - indexados)
    extras = len(indexados - esperados)
    print(f"Documentos preparados: {len(ids)}")
    print(f"Documentos indexados: {len(indexados)}")
    print(f"Documentos ausentes no índice: {faltantes}")
    print(f"Documentos extras no índice: {extras}")
    if faltantes or extras:
        print("O índice não corresponde ao arquivo preparado.")
        return False
    print("Os identificadores do índice correspondem ao arquivo preparado.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compara os documentos preparados com o índice local.")
    parser.add_argument("origem", type=Path, help="Arquivo JSONL preparado")
    parser.add_argument("banco", type=Path, help="Diretório do banco Chroma")
    argumentos = parser.parse_args()
    if not verificar(argumentos.origem, argumentos.banco):
        sys.exit(1)
