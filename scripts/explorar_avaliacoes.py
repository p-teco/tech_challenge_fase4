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
        tamanhos_titulos = []
        ids = Counter()
        pares = Counter()
        linhas_com_texto = Counter()
        notas_com_mensagem = Counter()
        for linha in leitor:
            total += 1
            preenchidos.update(campo for campo, valor in linha.items() if valor and valor.strip())
            notas[linha["review_score"]] += 1
            titulo = linha["review_comment_title"].strip()
            mensagem = linha["review_comment_message"].strip()
            tipos_texto[(bool(titulo), bool(mensagem))] += 1
            com_texto += bool(titulo or mensagem)
            if titulo or mensagem:
                ids[linha["review_id"]] += 1
                pares[(linha["review_id"], linha["order_id"])] += 1
                linhas_com_texto[tuple(linha.values())] += 1
            if titulo:
                tamanhos_titulos.append(len(titulo))
            if mensagem:
                tamanhos.append(len(mensagem))
                notas_com_mensagem[linha["review_score"]] += 1

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
    print("\nIdentificadores nas avaliações com texto:")
    print(f"  review_id distintos: {len(ids)}")
    print(f"  review_id repetidos: {sum(quantidade > 1 for quantidade in ids.values())}")
    print(f"  Registros com review_id repetido: {sum(quantidade for quantidade in ids.values() if quantidade > 1)}")
    print(f"  Pares review_id e order_id distintos: {len(pares)}")
    print(f"  Pares repetidos: {sum(quantidade > 1 for quantidade in pares.values())}")
    print(f"  Registros com par repetido: {sum(quantidade for quantidade in pares.values() if quantidade > 1)}")
    print(f"  Linhas completas duplicadas excedentes: {sum(quantidade - 1 for quantidade in linhas_com_texto.values())}")
    if tamanhos_titulos:
        print("\nTamanho dos títulos em caracteres:")
        print(f"  Mínimo: {min(tamanhos_titulos)}")
        print(f"  Mediana: {median(tamanhos_titulos):g}")
        print(f"  Máximo: {max(tamanhos_titulos)}")
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
    print("\nDistribuição de notas das avaliações com mensagem:")
    for nota, quantidade in sorted(notas_com_mensagem.items()):
        print(f"  {nota}: {quantidade}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resume o arquivo de avaliações da Olist.")
    parser.add_argument("arquivo", type=Path, help="Caminho do CSV de avaliações")
    resumir(parser.parse_args().arquivo)
