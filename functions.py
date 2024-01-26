# Importações
from collections import Counter
from rich.console import Console
from rich.table import Table
import sys

# Define a tabela de print
table = Table(show_header=True, header_style="bold magenta")

# Adiciona as colunas na tabela
table.add_column("Caractere", style="dim", width=12)
table.add_column("Low", style="dim", width=12)
table.add_column("High", style="dim", width=12)

# ! A função analisa_arquivo recebe um nome de arquivo como entrada, lê o conteúdo do arquivo, 
# ! conta a frequência de cada caractere na string e retorna um dicionário com as chaves sendo 
# ! os caracteres e os valores sendo as contagens. Além disso, a função também retorna o tamanho 
# ! do arquivo em bytes.
def analisa_arquivo(filename: str):
        
    # Abri o arquivo em modo de leitura
    with open(filename, 'r', encoding='utf-8') as arquivo:
        
        # Lê o conteúdo do arquivo, indo byte por byte
        conteudo = arquivo.read()
        
        # ? O Counter conta a frequência de cada caractere na string e retorna um 
        # ? dicionário com as chaves sendo os caracteres e os valores sendo as contagens.
        
        frequencia_caracteres = Counter(conteudo)
        tamanho = arquivo.tell()
        
    # Verifica se o arquivo foi lido corretamente, se não, finaliza o programa
    if not frequencia_caracteres:
        print(f"Arquivo '{filename}' não foi lido corretamente.")
        sys.exit(1)
    else:
        return frequencia_caracteres, tamanho

def separa_caracteres(caracteres: str, frequencia: int, tamanho: int):

    # Criação de listas para armazenar os caracteres, frequência, probabilidade e acumulada
    list_caracteres_aux = []
    list_frequencia_aux = []
    list_probabilidade_aux = []
    
    # Separa os caracteres, frequência, probabilidade e acumulada em listas
    for caractere, frequencia in caracteres:
        
        list_caracteres_aux.append(caractere)
        list_frequencia_aux.append(frequencia)
        print(list_caracteres_aux)
        
        # ? A probabilidade é arredondada no algoritmo de codificação aritmética para evitar erros 
        # ? de precisão ao realizar operações matemáticas com números decimais
        list_probabilidade_aux.append(frequencia/tamanho)
       
    # VERIFICAR ISSO AQUI
    aux = list_caracteres_aux[4]
    list_caracteres_aux[4] = list_caracteres_aux[3]
    list_caracteres_aux[3] = aux   
     
    console = Console()
    
    # Junta as listas em uma tupla, no caso a de caracteres e frequência
    caracteres = list(zip(list_caracteres_aux, list_frequencia_aux))
    
    console.print(f"\n\nTupla de Caracteres e Frequência: {caracteres}", style="bold red")
    console.print(f"Lista de Probabilidade: {list_probabilidade_aux}", style="bold red")
    
    return list_caracteres_aux, list_frequencia_aux, list_probabilidade_aux

def acumulada_generator(list_probabilidade: list, acumulada: list):
    
    # Adiciona o primeiro elemento da lista de probabilidade na lista acumulada sendo 0
    acumulada = [0]
    
    # Adiciona os elementos da lista de probabilidade na lista acumulada, somando com o elemento anterior
    for prob in list_probabilidade:
        
        # Soma o último elemento da lista acumulada com o elemento atual da lista de probabilidade
        acumulada.append(acumulada[-1] + prob)
        
    acumulada.append(sum(list_probabilidade))

    acumulada = acumulada[:-1] # VERIFICAR ISSO AQUI
    
    console = Console()
    console.print(f"Lista Acumulada: {acumulada}\n", style="bold red")
    
    return acumulada

# ! O código verifica se o caracter atual é igual a um dos caracteres da lista caracteres_lidos. 
# ! Se for, ele calcula novos valores de low e high com base no índice do caractere correspondente
# ! na lista acumulada. 
def codifica_aritmetica(caracteres_lidos: list, acumulada: list, arquivo: str):
    
    # Define o console para o print
    console = Console()
        
    def comparar_primeiros_digitos(numero1: int, numero2: int):
        
        # ! Comparar_primeiros_digitos(), compara se os primeiros dígitos dos dois números forem iguais, 
        # ! a função retorna True; caso contrário retorna False.
        
        return str(numero1)[0] == str(numero2)[0]
    
    def remover_primeiro_digito(numero: int):
        
        # ! Remover_primeiro_digito() que recebe um número como entrada e remove o primeiro dígito desse número. 
        # ! O primeiro dígito removido é retornado como um número separado, enquanto o número sem o primeiro dígito 
        # ! é retornado como o resultado da função.
        
        str_numero = str(numero)
        return int(str_numero[1:]), int(str_numero[0])
    
    def calculo_precisao_finita(new_low: int, list_vetor_aux: list):
        # Separa a variavel new_low em uma lista de caracteres
        new_low = list(str(new_low))
        
        # Percorre a lista de caracteres de new_low e verifica se tem um 0, se sim ele remove
        for i in new_low:
            if i == '0':
                new_low.remove(i)
        
        # Da append nos valores um por um da lista de new_low na lista list_vetor_aux
        for i in new_low:
            list_vetor_aux.append(int(i))
            
        return list_vetor_aux
    
    with open(arquivo, 'r', encoding='utf-8') as arquivo:
    
        # Inicializa low e high, definindo como maior valor possível e menor valor possível
        high = 9999
        low = 0
        list_vetor_aux = []
        caracter = arquivo.read(1)
        
        # Printa o valor de low e high iniciais
        table.add_row(f"-", f"{low}", f"{high}")

        # ? A cada iteração, ele verifica se o caractere atual é igual ao caractere desejado caracter. 
        # ? Se for, ele calcula novos valores para as variáveis new_low e new_high usando a fórmula 
        # ? - new_low = low + (high-low+1) * acumulada[i]
        # ? - new_high = low + (high-low+1) * acumulada[i+1] - 1
        for i, c in enumerate(caracteres_lidos):
        
            if caracter == c:
                new_low = int(low + (high-low+1) * acumulada[i])
                new_high = int(low + (high-low+1) * acumulada[i+1] - 1)
                
                # Printa os valores de low e high para o seu caractere correspondente
                table.add_row(f"{c}", f"{new_low}", f"{new_high}")
                
                break
        
           
        # * Em cada iteração desse loop, há um loop while interno que compara os primeiros dígitos de dois 
        # * números, new_low e new_high.         
        while caracter:
            
            # Lê o próximo caractere dentro do arquivo
            caracter = arquivo.read(1)
        
            # ? Se os primeiros dígitos forem iguais, um conjunto de operações é executado, incluindo a remoção 
            # ? do primeiro dígito de new_low e new_high, a adição de um valor à lista list_vetor_aux e a atualização 
            # ? dos valores de new_low e new_high. 
        
            while comparar_primeiros_digitos(new_low, new_high):
                
                # Remover o primeiro dígito de new_low e new_high
                new_low, saida = remover_primeiro_digito(new_low)
                new_high, saida = remover_primeiro_digito(new_high)
                
                # Adicionar o primeiro dígito removido à lista list_vetor_aux
                list_vetor_aux.append(saida)
                
                # Atualiza os novos valores de new_low e new_high
                new_low = new_low * 10
                new_high = new_high * 10 + 9
                
                # Printa os valores atualizados
                table.add_row(f"-", f"{new_low}", f"{new_high}")

            # ? For que itera sobre os caracteres lidos anteriormente e verifica se o caractere atual é igual a 
            # ? algum dos caracteres na lista. Se for encontrado um caractere correspondente, algumas operações 
            # ? são realizadas com base nos valores de new_low, new_high e acumulada
            for i, c in enumerate(caracteres_lidos):
                
                if caracter == c:
                    
                    # Salva o valor de new_low antes de ser atualizado
                    original_new_low = new_low
                    
                    # Atualiza os novos valores de new_low e new_high
                    new_low = int(new_low + ((new_high-new_low+1) * acumulada[i]))
                    new_high = int(original_new_low + ((new_high-original_new_low+1) * acumulada[i+1]) - 1)
                    
                    # Printa os valores de low e high para o seu caractere correspondente
                    table.add_row(f"{c}", f"{new_low}", f"{new_high}")

                    break
    
    console.print(table)
    
    # Calcula a precisão finita do new_low
    list_vetor_aux = calculo_precisao_finita(new_low, list_vetor_aux)
    
    # Retira o último elemento da lista_vetor_aux
    list_vetor_aux.pop()
    
    return list_vetor_aux
