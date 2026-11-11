import argparse
import csv
import json
from pathlib import Path


def preparar(origem, destino):
    documentos = []
    identificadores = set()

    with origem.open(encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        campos = {"review_id", "order_id", "review_score", "review_comment_title", "review_comment_message"}
        if not campos.issubset(leitor.fieldnames or []):
            raise ValueError("O CSV não contém os campos necessários para a preparação.")

        for linha in leitor:
            titulo = (linha["review_comment_title"] or "").strip()
            mensagem = (linha["review_comment_message"] or "").strip()
            if not titulo and not mensagem:
                continue

            review_id = (linha["review_id"] or "").strip()
            order_id = (linha["order_id"] or "").strip()
            if not review_id or not order_id:
                raise ValueError(f"Identificador ausente na linha {leitor.line_num}.")
            nota = (linha["review_score"] or "").strip()
            if nota not in {"1", "2", "3", "4", "5"}:
                raise ValueError(f"Nota inválida na linha {leitor.line_num}: {nota!r}")
            par = (review_id, order_id)
            if par in identificadores:
                raise ValueError(f"Par de identificadores repetido na linha {leitor.line_num}: {par}")
            identificadores.add(par)
            documentos.append({"review_id": review_id, "order_id": order_id, "review_score": int(nota), "texto": "\n".join(parte for parte in (titulo, mensagem) if parte)})

    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("x", encoding="utf-8", newline="\n") as arquivo:
        for documento in documentos:
            arquivo.write(json.dumps(documento, ensure_ascii=False) + "\n")
    print(f"Documentos preparados: {len(documentos)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepara as avaliações para a base de conhecimento.")
    parser.add_argument("origem", type=Path, help="Caminho do CSV de avaliações")
    parser.add_argument("destino", type=Path, help="Caminho do arquivo JSONL a criar")
    argumentos = parser.parse_args()
    preparar(argumentos.origem, argumentos.destino)
