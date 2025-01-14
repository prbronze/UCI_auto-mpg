import numpy as np

pesos = np.random.rand(10,3)

ent1 = np.array([
        [1,1,1,0,0,0,0,0,0,0],
        [1,1,0,1,0,0,0,0,0,0],
        [1,1,0,0,1,0,0,0,0,0]]) 

ent2 = np.array([
        [0,0,0,0,0,0,0,1,1,1],
        [0,0,0,0,0,0,1,0,1,1],
        [0,0,0,0,0,1,0,0,1,1]])

ent3 = np.array([
        [0,0,0,1,1,1,0,0,0,0],
        [0,0,0,1,1,0,1,0,0,0],
        [0,0,0,1,1,0,0,1,0,0]])

'''Conclusão 1: A escolha foi feita de maneira a manter um grau de sobreposição entre cada uma dos vetores de cada entrada.
Tendo 3 neurônios ativos consideramos então a possibilidade de permutar a posição de 1 dos 3 neurônios ativos.
Espera-se que dessa forma estas entradas sejam clusterizadas ao redor do mesmo neurônio.'''

#ambos juntam todos em uma matriz
entradas = np.vstack([ent1,ent2,ent3])
#np.concatenate((ent1,ent2,ent3),axis=0)
print(f'\nOs pesos de cada um dos 3 neurônios são :\n {pesos}')
print(f'\nA matriz de todas as 9 entradas de exemplo é :\n {entradas}')

def redeCompetitiva(X,W):
    '''
    Esta função itera ao longo da matriz X calculando o produto vetorial em relação a cada
    um dos vetores contidos em W (peso dos neurônios).
    Imprimindo qual neurônio foi mais ativado (ganhador) por cada um dos vetores de entrada.
    '''

    H = np.dot(ent1,W) #tranposição para produto vetorial
    winners = H.argsort()[:,-1]
    print ('Para o conjunto de entradas:\n', X ,'\nE pesos\n', W,
                   '\nOs neurônios vencedores são respectivamente:\n', winners)

redeCompetitiva(ent1,pesos)
redeCompetitiva(ent2,pesos)
redeCompetitiva(ent3,pesos)

#Próximo passo é escrever um algoritmo para treinar esta rede
# de tal forma que os neurônios se agrupem formando clusters.

def treinaCompetitiva(X,W):
    #Treinar
    nExemplos = X.shape[0]
    for step in range(4000):
        ex = np.random.randint(nExemplos)
        h = np.dot(W,X[ex]) #lista de produto vetorial
        winner = h.argsort()[-1]
        alpha = 0.05 # convergindo de forma suave
        dw = alpha*(W[winner]*X[ex]) #loss
        W[winner] += dw
        #normalizando um a um
        for w in range(W.shape[0]):
            W[w] = W[w]/np.linalg.norm(W[w])

    #Imprimi pesos finais e posições destes pesos
    for w in range(W.shape[0]):
        print(f'Os pesos atualizados do neurônio {w+1} são:\n {W[w]}')
        print(f'Os dois maiores pesos neste caso estão localizados nas posições:\n {W.argsort()[w][:-3:-1]}\n')
    
    return W

#Testando para os exemplos anteriores
novos_pesos    = treinaCompetitiva(entradas,pesos)
redeCompetitiva(entradas,novos_pesos)

'''Conlcusão 2: Utilizando-se um alpha pequeno e uma quantidade razoável de interações conseguiu-se
a garantia de uma solução convergente. Quando alimentamos uma a uma as entradas para o 
a rede treinada ela consegue atribuir a cada um dos neurônios que melhor ativam para si.'''

#Gerador de exemplos
def generateExamples(nExamples, inputSize, patternSize):
    '''
    Esta função gera uma quantidade nExamples de exemplos de vetores de tamanho inputSize.
    Sendo que seu padrão deve apresentar um número patternSize de neurônios ativos.
    '''
    a = np.zeros(inputSize-patternSize)
    a = np.append(a,np.ones(patternSize))
    entradas = np.zeros([nExamples,inputSize]);
    for i in range(nExamples):
        entradas[i]  = np.random.permutation(a) 
    return entradas

novas_entradas = generateExamples(20,10,3)

print(f'Gerando 20 novas entradas:\n {novas_entradas}')

#testa com novos pesos
redeCompetitiva(novas_entradas,novos_pesos)
