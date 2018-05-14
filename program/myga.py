import random
import copy

# Global
numeroCromossomos = 5
populacao = 6
geracoes = 100


def functionX(x):
    return x**2


def definirCromossomo():
    cromossomo = []
    for _ in range(numeroCromossomos):
        if random.random() >= 0.5:
            cromossomo.append(1)
        else:
            cromossomo.append(0)

    return cromossomo


def converterCromossomo(cromossomo):
    decimal = ''.join(str(x) for x in cromossomo)
    return int(decimal, 2)


class Agent(object):
    def __init__(self):
        self.cromossomoBIT = definirCromossomo()
        self.cromossomoINT = converterCromossomo(self.cromossomoBIT)
        self.fitnessPercent = 0.0
        self.rangeRoleta = [0.0, 0.0]
        self.fitness = -1

    def __str__(self):
        return "CromossomoBIT: {} CromossomoINT: {} Fitness: {} FitnessPercent: {} RangeRoleta: {}".format(self.cromossomoBIT, self.cromossomoINT, self.fitness, self.fitnessPercent, self.rangeRoleta)


def iniciarPopulacao(populacao):
    return [Agent() for _ in range(populacao)]


def definirFitness(agents):
    for agent in agents:
        agent.fitness = functionX(agent.cromossomoINT)
    return agents


def calcularFitnessPercent(agents):
    somatorio = 0
    for agent in agents:
        agent.fitnessPercent = 0.0
    for x in agents:
        somatorio += x.fitness

    for agent in agents:
        agent.fitnessPercent = ((agent.fitness * 100) / somatorio)
    return agents


def definirRangeRoleta(agents):
    for agent in agents:
        agent.rangeRoleta = [0.0, 0.0]
    agents = sorted(agents, key=lambda x: x.fitnessPercent)
    # print("ANTES DO FOR")
    # print('\n'.join(map(str, agents)))
    somatorio = 0
    for x in range(populacao):
        if x == 0:
            somatorio += agents[x].fitnessPercent
            agents[x].rangeRoleta[1] = somatorio
            agents[x].rangeRoleta[0] = 0.0
        else:
            agents[x].rangeRoleta[0] = somatorio
            agents[x].rangeRoleta[1] = (somatorio + agents[x].fitnessPercent)
            somatorio += agents[x].fitnessPercent
    # print("DEPOIS DO FOR")
    # print('\n'.join(map(str, agents)))

    return agents


def selecao(agents):
    listaSelecionados = []
    agents = sorted(agents, key=lambda x: x.fitnessPercent)
    # print('\n'.join(map(str, agents)))
    # listaSelecionados.append(agents[-1])  # Elitismo

    for _ in range(populacao):
        numeroAleatorio = random.uniform(0.0, 100.0)
        for agent in agents:
            if numeroAleatorio >= agent.rangeRoleta[0] and numeroAleatorio < agent.rangeRoleta[1]:

                # Todos os objetos que eu quero adicionar na lista, tem que
                # ser novos objetos e não cópias dos q já existem
                agenteSelecionado = copy.deepcopy(agent)
                listaSelecionados.append(agenteSelecionado)
                del agent  # Destruo o obj antigo pra liberar memória
                break

    for x in listaSelecionados:
        print("SELECIONADO", x)

    agents = listaSelecionados

    print('\n'.join(map(str, agents)))

    return agents


def crossover(agents):
    list = [*range(populacao)]

    TAXACROSS = int(0.8*populacao)

    for _ in range(int(TAXACROSS/2)):  # Crossando sempre 80% da populacao
        indexPai = random.choice(list)
        pai = agents[indexPai]
        list.remove(indexPai)

        indexMae = random.choice(list)
        list.remove(indexMae)
        mae = agents[indexMae]

        child1 = Agent()
        child2 = Agent()
        split = random.randint(0, numeroCromossomos)
        child1.string = pai.cromossomoBIT[0:split] + mae.cromossomoBIT[split:numeroCromossomos]
        child2.string = mae.cromossomoBIT[0:split] + pai.cromossomoBIT[split:numeroCromossomos]

        agents.remove(mae)
        agents.remove(pai)

        agents.append(child1)
        agents.append(child2)

    return agents


def mutar(agents):
    for agent in agents:
        pontoCorte = random.randint(0, numeroCromossomos-1)  # Gero um ponto de corte aleatorio
        chanceMutacao = random.random()
        if chanceMutacao <= 0.01:  # Chance de mutacao em 0.01
            print("VOU MUTAR >> ", agent.cromossomoBIT)
            if agent.cromossomoBIT[pontoCorte] == 0:
                agent.cromossomoBIT[pontoCorte] = 1
                print("MUTADO >> ", agent.cromossomoBIT)
            else:
                agent.cromossomoBIT[pontoCorte] = 0
                print("MUTADO >> ", agent.cromossomoBIT)

    return agents


def execGA():
    agents = iniciarPopulacao(populacao)  # Inicio uma populacao aleatoria

    for geracao in range(geracoes):
        print("Geracao " + str(geracao))

        agents = definirFitness(agents)  # Defino a fitness
        agents = calcularFitnessPercent(agents)  # Calculo o percentual na rolate
        agents = definirRangeRoleta(agents)  # Defino o range na roleta
        agents = selecao(agents)  # Seleciono novos individuos a partir da geracao anterior
        agents = crossover(agents)  # Crosso esses individuos
        agents = mutar(agents)  # Muto eles

        if any(agent.fitness >= 961 for agent in agents):
            print('Achei um bom')
            exit(0)


execGA()
