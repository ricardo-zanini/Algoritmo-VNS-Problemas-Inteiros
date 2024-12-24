import random
import numpy as np
import os 
import time
import timeit

from itertools import combinations
from random import randint


# =================== Retorna o valor de uma dada solução ======================
def solution_value(solution):
    value = 0
    for i in range(len(solution)):
        value = value + ((solution[i] * (solution[i] + 1)) / 2)
    return value


# =================== Criação de solução básica inicial ========================
def create_initial_solution(bottle_number, bottle_lower_bounds, bottle_upper_bounds):
    initial_solution = []
    balls_count = 0

    for bottle in range(int(bottle_number)):
        random_number_of_balls = bottle_lower_bounds[bottle]
        initial_solution.append(random_number_of_balls)

        balls_count = balls_count + random_number_of_balls

    while balls_count < balls_number:
        for bottle in range(int(bottle_number)):
            number_balls_add = bottle_upper_bounds[bottle] - initial_solution[bottle]

            if(number_balls_add > (balls_number - balls_count)):
                number_balls_add = balls_number - balls_count

            rand_balls_add = randint(0, number_balls_add)
            initial_solution[bottle] = initial_solution[bottle] + rand_balls_add

            balls_count = balls_count + rand_balls_add
    return initial_solution

# =================== Verificação de qual critério de parada foi selecionado e para com base nele ===================
def criterion_verify(time_criterion_selected, time_stop_criterion, time_start, interactions_stop_criterion, iteractions_number):
    time_now = timeit.default_timer()
    if(time_criterion_selected):
        if((time_now - time_start) >= time_stop_criterion):
            print("Executado em " + str(time_now - time_start) + " segundos")
            return False
        else:
            return True
    else:
        if(iteractions_number >= interactions_stop_criterion):
            print("Executado em " + str(time_now - time_start) + " segundos")
            return False
        else:
            return True

# =================== Procura K viznhança de uma solução enviada ========================
def neighborhood(solution, k, bottle_lower_bounds, bottle_upper_bounds):
    
    # Gerar os índices da lista
    indexes = range(len(solution))
    
    # Gerar lista de combinações de índices
    combinations_1 = list(combinations(indexes, k))
    combinations_1_len = len(combinations_1[0])

    # Ultimo elemento de cada combinação em que será retirada uma bola, os elementos seguintes receberão bolas
    last_comb_get = np.floor(combinations_1_len / 2) - 1

    # Começa com vizinhanca vazia
    neighborhood = []
    for i in combinations_1:                            
        add = 1                                    
        new_neighbor = solution.copy()             
        for comb_1_el in range(len(i)):                                         
            if(comb_1_el <= last_comb_get):                                                     # Se o índice atual <= do que ultimo indice de tirar bolas, então tira bolas
                value_get = 1
                if(combinations_1_len % 2 == 1 and comb_1_el == last_comb_get):                 # Se o tamanho da combinação for impar, retira 2 elementos do ultimo get
                    value_get = 2
                if(new_neighbor[i[comb_1_el]] - value_get < bottle_lower_bounds[i[comb_1_el]]): # Se ao retirar bolas ferimos o limite inferior, selecao é invalida
                    add = 0
                else:
                    new_neighbor[i[comb_1_el]] = new_neighbor[i[comb_1_el]] - value_get         # Senao retiamos bolas
            else:                                                                               # Coloca bolas nesses índices
                if(new_neighbor[i[comb_1_el]] == bottle_upper_bounds[i[comb_1_el]]):            # Se ao adicionarmos bolas ferimos limite superior, seleção é invalida
                    add = 0
                else:
                    new_neighbor[i[comb_1_el]] = new_neighbor[i[comb_1_el]] + 1                 # Senao adicionamos bolas
        if add == 1:
            neighborhood.append(new_neighbor)
                
    return neighborhood

# =================== Gera busca local buscando mínimo local ====================
def local_search(solution, neighborhood):
    best_solution = solution

    while(True):
        best_solution_after_loop = best_solution

        for neighbor in neighborhood:
            if(solution_value(neighbor) > solution_value(best_solution)):
                best_solution = neighbor
                break
        if(solution_value(best_solution) <= solution_value(best_solution_after_loop)):
            break
    return best_solution

# =================== Objetivo: andar K passos aleatorios numa vizinhanca, gerando perturbacao na solução ==================
def shake(solution, k, bottle_lower_bounds, bottle_upper_bounds):
    # Constante de aumento de perturbação
    c = 2
    # Deve-se fazer um shake de k passos na vizinhança
    solution_shake = solution

    # Gerar os índices da lista
    indexes = range(len(solution_shake))
    
    # Gerar lista de combinações de índices
    combinations_1 = list(combinations(indexes, k))
    combinations_1_len = len(combinations_1[0])

    # Ultimo elemento de cada combinação em que será retirada uma bola, os elementos seguintes receberão bolas
    last_comb_get = np.floor(combinations_1_len / 2) - 1

    count = 0

    while count < c*k:            
        add = 1                                    
        new_solution = solution_shake.copy()    
        i = combinations_1[randint(0, len(combinations_1) - 1)]
        for comb_1_el in range(len(i)):                                         
            if(comb_1_el <= last_comb_get):                                                     # Se o índice atual <= do que ultimo indice de tirar bolas, então tira bolas
                value_get = 1
                if(combinations_1_len % 2 == 1 and comb_1_el == last_comb_get):                 # Se o tamanho da combinação for impar, retira 2 elementos do ultimo get
                    value_get = 2
                if(new_solution[i[comb_1_el]] - value_get < bottle_lower_bounds[i[comb_1_el]]): # Se ao retirar bolas ferimos o limite inferior, selecao é invalida
                    add = 0
                else:
                    new_solution[i[comb_1_el]] = new_solution[i[comb_1_el]] - value_get         # Senao retiamos bolas
            else:                                                                               # Coloca bolas nesses índices
                if(new_solution[i[comb_1_el]] == bottle_upper_bounds[i[comb_1_el]]):            # Se ao adicionarmos bolas ferimos limite superior, seleção é invalida
                    add = 0
                else:
                    new_solution[i[comb_1_el]] = new_solution[i[comb_1_el]] + 1                 # Senao adicionamos bolas
        if add == 1:
            solution_shake = new_solution
            count = count + 1

    return solution_shake

# ================= Solicitação de dados do usuário ==================

file_name                       = input("Arquivo txt com dados de entrada para o problema (no formato padrão):")

time_stop_criterion             = input("Critério de parada por tempo em segundos:")
interactions_stop_criterion     = input("Critério de parada por número de iterações:")
time_criterion_selected         = True

seed                            = input("Semente aleatória:")


# ============== Verifica se parametros foram preenchidos ============
if (str(time_stop_criterion) != "" and str(interactions_stop_criterion) != ""):
    print("ERRO - Você selecionou mais de um critério de parada!!")
    exit()

if (str(time_stop_criterion) == "" and str(interactions_stop_criterion) == ""):
    print("ERRO - Você nao selecionou um critério de parada!!")
    exit()


# ================ Verifica se parâmetros são números ================
if(str(time_stop_criterion) != ""):
    try:
        time_stop_criterion = int(time_stop_criterion)
        time_criterion_selected = True
    except:
        print("ERRO - Critério de tempo não pôde ser convertido em número")
        exit()
else:
    try:
        interactions_stop_criterion = int(interactions_stop_criterion)
        time_criterion_selected = False
    except:
        print("ERRO - Critério de número iterações não pôde ser convertido em número")
        exit()

try:
    seed = int(seed)
    rand = random.seed(seed)
except:
    print("ERRO - Semente aleatória não é um número")
    exit()


# =============== Abertura de Arquivo ====================
try:
    dir = os.path.dirname(os.path.realpath(__file__) ) 
    file_path = dir + "\\data\\" + file_name + ".txt"
    file = open(file_path)
except:
    print("ERRO - O arquivo txt com o caminho " + file_path + " não pôde ser aberto")
    exit()


# =============== Leitura de Arquivo ====================
try:
    bottle_number = int(file.readline())
    balls_number  = int(file.readline())

    bottle_lower_bounds = []
    bottle_upper_bounds = []

    for bottle in range(int(bottle_number)) :
        aux = file.readline().split(" ")
        bottle_lower_bounds.append(int(aux[0]))
        bottle_upper_bounds.append(int(aux[1]))
except:
    print("ERRO - Problema na leitura do arquivo")
    exit()


# =============== Solução Inicial Aleatória ====================
initial_solution = create_initial_solution(bottle_number, bottle_lower_bounds, bottle_upper_bounds)

# ----- Contagem de tempo ----- 
time_start = timeit.default_timer()
iteractions_number = 0

# =============== EXECUÇÃO DO ALGORITMO VNS ====================

solution = initial_solution.copy()
best_solution = []

m = 3
while criterion_verify(time_criterion_selected, time_stop_criterion, time_start, interactions_stop_criterion, iteractions_number):
    iteractions_number += 1
    k = 2
    while k <= m:

        solution_shaken         = shake(solution, k, bottle_lower_bounds, bottle_upper_bounds)
        neighbors               = neighborhood(solution_shaken, k, bottle_lower_bounds, bottle_upper_bounds)
        solution_new            = local_search(solution_shaken, neighbors)

        if(solution_value(solution_new) <= solution_value(solution)):
            k = k + 1
        else:
            solution = solution_new
            k = 2
        if(solution_value(solution) > solution_value(best_solution)):
            best_solution = solution

print("A melhor solução encontrada é:")
print(best_solution)
print("O valor da solução encontrada é:")
print(solution_value(best_solution))
