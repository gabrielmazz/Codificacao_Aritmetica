# Trabalho de PID - Codificação de Aritimética
# Gabriel Alves Mazzuco

# Para instalar as bibliotecas necessárias, execute o comando abaixo no terminal:
# ! pip install -r requirements.txt 

# Importações
import sys
from rich.console import Console

# Arquivos extras
import functions as f

# Criação de listas para armazenar os caracteres, frequência, probabilidade e acumulada
list_caracteres, list_frequencia, list_probabilidade, list_vetor = [], [], [], []

acumulada = []

# Main
if __name__ == "__main__":
    
    # TODO Leitura do arquivo por argumento
    # TODO python3 main.py {arquivo}
    if len(sys.argv) < 2:
        print("Por favor, informe o nome do arquivo como argumento.")
        sys.exit(1)

    filename = sys.argv[1]
    
    # Contagem da frequência de caracteres usando a função do arquivo functions.py
    frequencia, tamanho = f.analisa_arquivo(filename)
    
    # Criação de listas para armazenar os caracteres, frequência, probabilidade e acumulada
    caracteres = frequencia.items()
    
    # Separa os caracteres, frequência, probabilidade e acumulada em listas usando a função do arquivo functions.py
    list_caracteres, list_frequencia, list_probabilidade = f.separa_caracteres(caracteres, frequencia, tamanho)
    
    # Gera a lista acumulada usando a função do arquivo functions.py
    acumulada = f.acumulada_generator(list_probabilidade, acumulada)
    
    # Gera o vetor de saída usando a função do arquivo functions.py, todo o valor será a codificação aritmética
    list_vetor = f.codifica_aritmetica(list_caracteres, acumulada, filename)
    
    console = Console()
    console.print(f"\nVetor codificado: {list_vetor}\n\n", style="bold yellow")
    