import argparse
import csv
from collections import Counter
from pathlib import Path


def resumir(caminho):
    with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        colunas = leitor.fieldnames
        total = 0
        preenchidos = Counter()
        notas = Counter()
        com_texto = 0
        for linha in leitor:
            total += 1
            preenchidos.update(campo for campo, valor in linha.items() if valor and valor.strip())
            notas[linha["review_score"]] += 1
            com_texto += bool(linha["review_comment_title"].strip() or linha["review_comment_message"].strip())

    print(f"Total de avaliações: {total}")
    print("\nCampos preenchidos:")
    for coluna in colunas:
        print(f"  {coluna}: {preenchidos[coluna]}")
    print(f"\nAvaliações com título ou mensagem: {com_texto}")
    print("\nDistribuição de notas:")
    for nota, quantidade in sorted(notas.items()):
        print(f"  {nota}: {quantidade}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resume o arquivo de avaliações da Olist.")
    parser.add_argument("arquivo", type=Path, help="Caminho do CSV de avaliações")
    resumir(parser.parse_args().arquivo)
