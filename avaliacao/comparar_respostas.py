import argparse
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from buscar_avaliacoes import buscar, mostrar
from responder import responder


def main():
    parser = argparse.ArgumentParser(description="Compara respostas com 10, 25 e 50 avaliações recuperadas.")
    parser.add_argument("banco", type=Path, help="Diretório do banco Chroma")
    parser.add_argument("pergunta", help="Pergunta sobre as avaliações")
    parser.add_argument("--limites", type=int, nargs="+", choices=(10, 25, 50), default=[10, 25, 50], help="Quantidades a comparar")
    argumentos = parser.parse_args()
    chave = os.environ.get("NVIDIA_API_KEY")
    if not chave:
        sys.exit("Defina a variável NVIDIA_API_KEY antes de executar a avaliação.")

    try:
        maior_limite = max(argumentos.limites)
        resultados = buscar(argumentos.banco, argumentos.pergunta, maior_limite)
        if len(resultados) < maior_limite:
            sys.exit(f"A comparação requer pelo menos {maior_limite} avaliações recuperadas.")
        for limite in argumentos.limites:
            print(f"\nGerando resposta com {limite} avaliações...", flush=True)
            resposta = responder(argumentos.pergunta, resultados[:limite], chave)
            print(f"Resposta: {resposta}", flush=True)
    except HTTPError as erro:
        sys.exit(f"Erro HTTP {erro.code} ao consultar o serviço.")
    except (URLError, TimeoutError, ValueError, KeyError, IndexError, OSError) as erro:
        sys.exit(f"Não foi possível concluir a comparação: {erro}")

    print("\nAvaliações recuperadas:")
    for numero, resultado in enumerate(resultados, 1):
        print(f"\n[A{numero}]", end="")
        mostrar([resultado])


if __name__ == "__main__":
    sys.stdout.reconfigure(errors="backslashreplace")
    main()
