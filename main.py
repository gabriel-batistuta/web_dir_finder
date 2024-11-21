import requests
import itertools
import string
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore
import os

def gerar_combinacoes():
    letras = string.ascii_uppercase  # A-Z
    for letras_comb in itertools.product(letras, repeat=4):  # Todas as combinações de 4 letras
        prefixo = ''.join(letras_comb)
        for numero in range(1000):  # Números de 000 a 999
            yield f"{prefixo}-{numero:03d}"  # Formato como "MIMK-160"

def testar_mp4(url, palavra, arquivo_saida):
    tentativa = f"{url.rstrip('/')}/{palavra}.mp4"
    try:
        response = requests.head(tentativa, timeout=5)  # Requisição HEAD para economizar largura de banda
        if response.status_code == 200:
            print(f"{Fore.GREEN}[+]{Fore.RESET}: {Fore.YELLOW}{tentativa}{Fore.RESET}")
            # Escrever diretamente no arquivo de saída
            with open(arquivo_saida, 'a') as jav_file:
                jav_file.write(f"{tentativa}\n")
            return tentativa
        else:
            print(f"{Fore.RED}[-]{Fore.RESET}: {Fore.YELLOW}{tentativa}{Fore.RESET}")
    except requests.RequestException:
        pass
    return None

def fuzzing_mp4(url, arquivo_saida):
    combinacoes = gerar_combinacoes()

    # Use o número máximo de threads disponíveis no sistema
    max_threads = int(os.cpu_count()) - 2  # Um número razoável de threads
    print(f"Usando {max_threads} threads para o fuzzing.")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(testar_mp4, url, palavra, arquivo_saida): palavra for palavra in combinacoes}

        for future in futures:
            future.result()  # Espera a execução de cada thread e garante que a URL válida seja escrita

# URL do diretório
url_diretorio = ""
arquivo_saida = "urls.txt"

# Realiza o fuzzing
print(f"Iniciando fuzzing para encontrar arquivos .mp4 em {url_diretorio}...")
fuzzing_mp4(url_diretorio, arquivo_saida)

print(f"\nFuzzing finalizado. URLs dos arquivos .mp4 foram salvas em {arquivo_saida}.")
