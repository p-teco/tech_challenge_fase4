import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


CASOS = [
    ("Com evidência", "Que problema ocorreu na entrega?", "[A1] Nota 1: O pedido chegou duas semanas atrasado."),
    ("Evidência insuficiente", "Por que o pedido atrasou?", "[A1] Nota 1: O pedido chegou duas semanas atrasado."),
    ("Fora do escopo", "Qual é a cotação do dólar hoje?", "[A1] Nota 5: Gostei do produto e da entrega."),
]


def main():
    parser = argparse.ArgumentParser(description="Avalia respostas com exemplos fictícios.")
    parser.add_argument("--modelo", default="nvidia/nemotron-3.5-super-vl-120b-a12b")
    modelo = parser.parse_args().modelo
    chave = os.environ.get("NVIDIA_API_KEY")
    if not chave:
        sys.exit("Defina a variável NVIDIA_API_KEY antes de executar a avaliação.")

    for nome, pergunta, evidencias in CASOS:
        print(f"Executando caso: {nome}...", flush=True)
        dados = json.dumps({
            "model": modelo,
            "messages": [
                {"role": "system", "content": "Responda em português apenas com base nas avaliações fornecidas. Cite os identificadores das avaliações utilizadas. Se as evidências não forem suficientes ou a pergunta estiver fora do escopo, explique que não é possível responder com os dados disponíveis. Não invente informações."},
                {"role": "user", "content": f"Pergunta: {pergunta}\nAvaliações:\n{evidencias}"},
            ],
            "max_tokens": 1024,
        }).encode("utf-8")
        requisicao = Request(
            "https://integrate.api.nvidia.com/v1/chat/completions", data=dados,
            headers={"Authorization": f"Bearer {chave}", "Content-Type": "application/json"},
        )
        try:
            with urlopen(requisicao, timeout=120) as resposta:
                resultado = json.load(resposta)
            resposta_texto = resultado["choices"][0]["message"].get("content")
            if not resposta_texto:
                raise ValueError("A API não retornou uma resposta textual.")
        except HTTPError as erro:
            sys.exit(f"A API retornou erro HTTP {erro.code} no caso '{nome}'.")
        except (URLError, TimeoutError, KeyError, IndexError, ValueError) as erro:
            sys.exit(f"Não foi possível concluir o caso '{nome}': {erro}")

        print(f"\n--- {nome} ---\nPergunta: {pergunta}\nAvaliações: {evidencias}\nResposta: {resposta_texto}", flush=True)


if __name__ == "__main__":
    main()
