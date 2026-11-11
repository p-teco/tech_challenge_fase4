import argparse
import csv
from collections import Counter
from pathlib import Path
from statistics import median


def resumir(caminho):
    with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        colunas = leitor.fieldnames
        total = 0
        preenchidos = Counter()
        notas = Counter()
        com_texto = 0
        tipos_texto = Counter()
        tamanhos = []
        for linha in leitor:
            total += 1
            preenchidos.update(campo for campo, valor in linha.items() if valor and valor.strip())
            notas[linha["review_score"]] += 1
            titulo = linha["review_comment_title"].strip()
            mensagem = linha["review_comment_message"].strip()
            tipos_texto[(bool(titulo), bool(mensagem))] += 1
            com_texto += bool(titulo or mensagem)
            if mensagem:
                tamanhos.append(len(mensagem))

    print(f"Total de avaliações: {total}")
    print("\nCampos preenchidos:")
    for coluna in colunas:
        print(f"  {coluna}: {preenchidos[coluna]}")
    print(f"\nAvaliações com título ou mensagem: {com_texto}")
    print("\nPresença de texto:")
    print(f"  Apenas título: {tipos_texto[(True, False)]}")
    print(f"  Apenas mensagem: {tipos_texto[(False, True)]}")
    print(f"  Título e mensagem: {tipos_texto[(True, True)]}")
    print(f"  Sem título e sem mensagem: {tipos_texto[(False, False)]}")
    if tamanhos:
        print("\nTamanho das mensagens em caracteres:")
        print(f"  Mínimo: {min(tamanhos)}")
        print(f"  Mediana: {median(tamanhos):g}")
        print(f"  Máximo: {max(tamanhos)}")
        print(f"  Até 10 caracteres: {sum(tamanho <= 10 for tamanho in tamanhos)}")
        print(f"  Até 20 caracteres: {sum(tamanho <= 20 for tamanho in tamanhos)}")
    print("\nDistribuição de notas:")
    for nota, quantidade in sorted(notas.items()):
        print(f"  {nota}: {quantidade}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resume o arquivo de avaliações da Olist.")
    parser.add_argument("arquivo", type=Path, help="Caminho do CSV de avaliações")
    resumir(parser.parse_args().arquivo)
