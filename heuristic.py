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

    for bottle in range(int(bottle_number)):
        number_balls_add = bottle_upper_bounds[bottle] - initial_solution[bottle]

        if(number_balls_add > (balls_number - balls_count)):
            number_balls_add = balls_number - balls_count
        
        initial_solution[bottle] = initial_solution[bottle] + number_balls_add

        balls_count = balls_count + number_balls_add

        if(balls_count == balls_number):
            break
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

    
    # Gerar duas listas de combinações de índices
    combinations_1 = list(combinations(indexes, k))
    combinations_2 = list(combinations(indexes, k))

    # Começa com vizinhanca vazia
    neighborhood = []
    for i in combinations_1:                            # faz loop pela primeira lista de combinações de indices (listas que tiram bolas)
        for j in combinations_2:                        # faz loop pela segunda lista de combinações de indices (listas que adicionam bolas)
            add = 1                                     # Inicia dizendo que pode adicionar resultado
            new_neighbor = solution.copy()              # Inicia novo vizinho
            for comb_1_el in i:                         # Loop por valores nas combinaçoes de L1
                for comb_2_el in j:                     # Loop por valores nas combinaçoes de L2
                    if(
                        comb_1_el == comb_2_el                                           # se algum dos elementos da L1 for igual a L2 significa que estamos tirando e colocando no mesmo pote logo não add
                        or new_neighbor[comb_1_el] == bottle_lower_bounds[comb_1_el]     # se estiver no limite inferior n pode tirar
                        or new_neighbor[comb_2_el] == bottle_upper_bounds[comb_2_el]     # se estiver no limite superior n pode colocar
                    ):                                         
                        add = 0
            if add == 1:
                for comb_1_el in i:  
                    new_neighbor[comb_1_el] = new_neighbor[comb_1_el] - 1
                for comb_2_el in j:     
                    new_neighbor[comb_2_el] = new_neighbor[comb_2_el] + 1

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

# =================== Objetivo: andar K passos aleatorios numa vizinhanca, gerando perturbacao na solução final ==================
def shake(solution, k, bottle_lower_bounds, bottle_upper_bounds):
    # Constante de aumento de perturbação
    c = 10
    # Deve-se fazer um shake de k passos na vizinhança
    solution_shake = []
    for i in range(k * c):
        solution_shake_list = neighborhood(solution, 1, bottle_lower_bounds, bottle_upper_bounds)
        solution_shake = solution_shake_list[random.randint(0, len(solution_shake_list) - 1)]
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

solution = initial_solution
best_solution = []

while criterion_verify(time_criterion_selected, time_stop_criterion, time_start, interactions_stop_criterion, iteractions_number):
    iteractions_number += 1
    k = 1
    m = 2
    while k <= m:
        print(k)
        solution_shaken = shake(solution, k, bottle_lower_bounds, bottle_upper_bounds)

        solution_new = local_search(solution_shaken, neighborhood(solution_shaken, k, bottle_lower_bounds, bottle_upper_bounds))

        if(solution_value(solution_new) <= solution_value(solution)):
            k = k + 1
        else:
            solution = solution_new
            k = 1
        if(solution_value(solution) > solution_value(best_solution)):
            best_solution = solution

print("A melhor solução encontrada foi:")
print(best_solution)
print("O valor da solução encontrada é:")
print(solution_value(best_solution))
