import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from buscar_avaliacoes import buscar, mostrar


if __name__ == "__main__":
    sys.stdout.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Compara os primeiros 10, 25 e 50 resultados da busca.")
    parser.add_argument("banco", type=Path, help="Diretório do banco Chroma")
    parser.add_argument("pergunta", help="Pergunta para a busca semântica")
    argumentos = parser.parse_args()
    resultados = buscar(argumentos.banco, argumentos.pergunta, 50)
    print(f"Pergunta: {argumentos.pergunta}\nResultados encontrados: {len(resultados)}")
    faixas = {1: "1 a 10", 11: "11 a 25", 26: "26 a 50"}
    for posicao, resultado in enumerate(resultados, 1):
        if posicao in faixas:
            print(f"\n--- Resultados {faixas[posicao]} ---")
        print(f"\nResultado {posicao}:", end="")
        mostrar([resultado])
