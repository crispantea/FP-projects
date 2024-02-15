def limpa_texto(texto):
    """
    Função limpa_texto: cad. carateres → cad. carateres

    Esta funcão limpa a cadeia de carácteres recebida, 
    isto é, remove os carateres brancos.
    """
    texto = ' '.join(((texto.strip()).split()))
    return texto
    
def corta_texto(texto, largura):
    """
    Função corta_texto: cad. carateres × inteiro → cad. carateres × cad. carateres

    Esta função corta o texto até à largura indicada
    de acordo com diferentes parâmetros.
    """
    texto1 = ""
    texto2 = ""
    texto = limpa_texto(texto)
    lista_do_texto = texto.split()
    if texto == "":
        texto1= ""
        texto2 = ""
        return(texto1, texto2)
    elif len(texto) == largura:
        texto1 = texto
        texto2 = ""
        return(texto1, texto2)
    elif len(lista_do_texto[0]) > largura:
        texto1 = ""
        texto2 = texto
        return (texto1, texto2)
    elif len(texto) < largura:
        texto1 = texto
        texto2 = ""
        return(texto1, texto2)
    elif texto[largura] == " ":
        texto1 = texto[:largura]
        texto2 = texto[largura + 1:]
        return (texto1, texto2)
    elif texto[largura] != 0:
        i = 0
        largura_sem_cortar_palavra = 0
        while texto[largura - i] != " ":
            largura_sem_cortar_palavra = largura - i
            i += 1
        texto1 = texto[:largura_sem_cortar_palavra - 1]
        texto2 = texto[largura_sem_cortar_palavra:]
        return (texto1, texto2)

def numero_de_palavras(texto):
    """
    Função numero_de_palavras: cad. carateres → inteiro

    Esta função recebe um texto qualquer e retorna o
    número de palavras desse texto.
    """
    texto = limpa_texto(texto)
    lista_do_texto = texto.split()
    numero_de_palavras = len(lista_do_texto)
    return numero_de_palavras

def insere_espacos(texto, largura):
    """
    Função insere_espacos: cad. carateres × inteiro→cad. carateres

    Esta função insere espaços até à largura indicada, se necessário.
    """
    texto = limpa_texto(texto)
    lista_do_texto = texto.split()
    n_espacos = largura - (len(texto))

    if numero_de_palavras(texto) == 1:
        resultado = lista_do_texto[0] + (n_espacos * " ")
        return resultado
    else:
    # Adiciona espaços até atingir a largura pretendida.
        while n_espacos > 0:
            i = 0
            while i < numero_de_palavras(texto) - 1:
                lista_do_texto[i] = lista_do_texto[i] + " "
                n_espacos -= 1
                i += 1
                if n_espacos == 0:
                    break
        return " ".join(lista_do_texto)

def verifica_justifica_texto(texto, largura):
    if type(texto) != str:
        raise ValueError("justifica_texto: argumentos invalidos")

    palavras_texto = (texto.strip()).split()

    if type(largura) != int or texto == "":
        raise ValueError("justifica_texto: argumentos invalidos")
    if largura <= 0 or len(palavras_texto[0]) > largura:
        raise ValueError("justifica_texto: argumentos invalidos")

def justifica_texto(texto, largura):
    """
    Função justifica_texto: cad. carateres × inteiro → tuplo

    Esta função recebe um texto e justifica-o de acordo com
    a largura inserida.
    """
    verifica_justifica_texto(texto, largura)
    texto = limpa_texto(texto)
    texto_cortado = corta_texto(texto, largura)
    lista_texto_cortado = list(texto_cortado)
    
    # Caso a frase limpa tenha uma linha e a largura pedida.
    if texto_cortado[1] == "" and len(texto_cortado[0]) == largura:
        return (texto_cortado[0],)
    # Caso a frase limpa tenha uma linha mas seja menor que a largura pedida.
    if texto_cortado[1] == "" and len(texto_cortado[0]) < largura:
        espacos_ness = largura - len(texto_cortado[0])
        return (texto_cortado[0] + " " * espacos_ness,)
    # Caso a frase limpa tenha mais de uma linha.
    if texto_cortado[1] != "":
        lista_res = []
        i = 0
        # Enquanto ainda haja texto para cortar:
        while len(lista_texto_cortado[1]) > largura:
            lista_res = lista_res + [lista_texto_cortado[0]]
            del lista_texto_cortado[0]
            lista_texto_cortado = list(corta_texto(lista_texto_cortado[0], largura))
        lista_res = lista_res + lista_texto_cortado
        # Adiciona espaços nos textos cortados se necessário.
        while i < len(lista_res) - 1:
            lista_res[i] = insere_espacos(lista_res[i], largura)
            i += 1
        # Adicionar à ultima linha os espaços necessários se for preciso.
        if len(lista_res[-1]) == largura:
            return tuple(lista_res)
        else:
            espacos_ness = largura - len(lista_res[-1])
            lista_res[-1] = lista_res[-1] + " " * espacos_ness
            return tuple(lista_res)

def calcula_quocientes(dic, deputados):
    """
    Função calcula quocientes: dicionário × inteiro → dicionário

    Esta função calcula os quocientes dos votos 
    apurados num circulo usando o método de Hondt.
    """
    dic_final = {}
    for partido in dic:
        i = 1
        valores = []
        # Cria a lista para o partido contendo os valores das sucessivas divisões.
        while i <= deputados:
            valores = valores + [dic[partido]/i]
            i += 1
        i = 0
        # Vai atribuir ao partido a respetiva lista de valores.
        dic_final[partido]=valores
    return dic_final

def compara(x):
    """
    Função compara: lista → float

    Esta função é uma função auxiliar para ajudar a
    ordenar uma lista de listas.
    """
    return -x[1]

def compara2(x):
    """
    Função compara: lista → int

    Esta função é uma função auxiliar para ajudar a
    ordenar uma lista de listas.
    """
    return x[2]

def atribui_mandatos(dic, deputados):
    """
    Função atribui_mandatos: dicionário × inteiro → lista
    
    Esta função atribui os mandatos de acordo com os votos apurados 
    num círculo eleitoral.
    """
    dicionario = calcula_quocientes(dic, deputados)
    lista_2 = []
    res = []
    valores_iguais = []
    valores_iguais_organizados = []
    for e in dicionario:
        for i in dicionario[e]:
            # Lista com listas de 2 elementos: (chave, valor).
            lista_2 = lista_2 + [[e] + [i]]
    lista_organizada = sorted(lista_2, key=compara)
    # Lista com listas de 3 elementos: (chave, valor, total de votos)
    for e in lista_organizada:
        e.append(dic[e[0]])
    if len(dic) == 1:
        for partido in dic:
            res = [partido] * deputados
        return res
    else:
        i = 0
        while i < deputados:
            # Se dois ou mais partidos tiverem dois valores iguais, ver quantos
            # mais têm esse mesmo valor.
            if lista_organizada[i][1] == lista_organizada[i+1][1]:
                j = 0
                # J conta o número de partidos com um certo valor igual.
                while lista_organizada[i][1] == lista_organizada[i+j][1]:
                    j += 1
                valores_iguais = lista_organizada[i:i+j]
                # Organizar esses partidos com igual valor de votos por ordem de
                # quem tem menor número total de votos.
                valores_iguais_organizados = sorted(valores_iguais, key=compara2)
                lista_organizada = lista_organizada[:i] + valores_iguais_organizados + lista_organizada[i+j:]
            res = res + [lista_organizada[i][0]]
            i += 1
        return res

def obtem_partidos(info):
    """
    Função obtem_partidos: dicionário → lista

    Esta função devolve a lista por ordem alfabética com
    o nome de todos os partidos que participaram nas eleições.
    """
    terriorio = ""
    res = []
    for e in info:
        for j in info[e]["votos"]:
            # Adicionar o partido ao resultado apenas se este já lá não estiver.
            if j not in res:
                res = res + [j]
    return sorted(res)

def compara3(x):
    """
    Função compara: lista → inteiro × inteiro

    Esta função é uma função auxiliar para ajudar a
    ordenar uma lista de listas.
    """
    return -x[2], -x[1]


def verifica_obtem_resultados_eleicoes(info):
    """
    Função verifica_obtem_resultado_eleicoes: dicionário → booleano

    Esta função é uma função auxiliar para verificar
    os argumentos na função obtem_resultado_eleicoes.
    """
    if type(info) != dict or len(info) <1:
        raise ValueError("obtem_resultado_eleicoes: argumento invalido")
    for circulo in info:
        if type(circulo) != str or type(info[circulo]) != dict or len(info[circulo]) != 2:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        if "deputados" not in info[circulo] or "votos" not in info[circulo]:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        if type(info[circulo]["deputados"]) != int or info[circulo]["deputados"] < 1:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        if type(info[circulo]["votos"]) != dict or len(info[circulo]["votos"]) < 1:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        for partidos in info[circulo]["votos"]:
            if type(partidos) != str:
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")
            if type(info[circulo]["votos"][partidos]) != int or info[circulo]["votos"][partidos] <= 0:
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")
    return True

def obtem_resultado_eleicoes(info):
    """
    Função obtem_resultado_eleicoes: dicionário → lista

    Esta função recebe um dicionário com a informação sobre as 
    eleiçoes num território com vários círculos eleitorais e 
    devolve a lista ordenada com os resultados das eleições.
    """
    verifica_obtem_resultados_eleicoes(info)

    dic_valores_tot = {}
    partidos = obtem_partidos(info)
    for e in partidos:
        dic_valores_tot[e] = {}

    # Obtem o valor total de votos de cada partido
    for circulo in info:
        for partido in info[circulo]["votos"]:
            #se o partido não tiver nenhum valor associado, associar o valor
            if dic_valores_tot[partido] == {}:
                valor = info[circulo]["votos"][partido]
                dic_valores_tot[partido] = valor
            #se o partido já tiver algum valor, associado, adicionar o novo valor ao valor antigo
            else:
                valor = info[circulo]["votos"][partido]
                dic_valores_tot[partido] = dic_valores_tot[partido] + valor
    # Obtém a lista com todos os mandatos de todos os circulos atribuídos
    total_mandatos_atribuidos = []
    for circulo in info: 
        total_mandatos_atribuidos += atribui_mandatos(info[circulo]["votos"], info[circulo]["deputados"])
    dic_mandatos = {}
    for e in partidos:
        dic_mandatos[e] = {}
    ordenados = sorted(total_mandatos_atribuidos)
    for partidos in dic_mandatos:
        dic_mandatos[partidos] = ordenados.count(partidos)
    # Cria a lista com as listas onde as ultimas contêm o nome do partido, o numero total de votos
    # e o numero de mandatos atribuidos
    lista_res = []
    for partido in dic_mandatos:
        lista_res = lista_res + [[partido, dic_mandatos[partido], dic_valores_tot[partido]]]

    lista_res = sorted(lista_res, key=compara3)
    i = 0
    while i < len(lista_res):
        lista_res[i] = tuple(lista_res[i])
        i += 1
    return lista_res


def produto_interno(tuplo1, tuplo2):
    """
    Função produto_interno: tuplo × tuplo → real

    Esta função devolve o resultado do produto interno 
    entre dois vetores.
    """
    produto_interno = 0
    for i in range(len(tuplo1)):
        produto_interno = produto_interno + tuplo1[i] * tuplo2[i]
    return float(produto_interno)

def verifica_convergencia(matriz, constantes, solucao, precisao):
    """
    Função verifica_convergencia: tuplo × tuplo × tuplo × real → booleano
    
    Esta função verifica a convergência entre os valores da 
    solução da matriz e a precisão pretendida. Retorna True 
    caso o valor absoluto do erro de todas as equações seja
    inferior à precisão, |fi(x)−ci| < ϵ, e False caso contrário.
    """
    lista_res = []
    res = 0
    i = 0
    j = 0
    for e in matriz: # Iterar pelas linhas da matriz
        while i < len(e): # Iterar pelas colunas da matriz
            res = res + (e[i] * solucao[i])
            i +=1
        # Cálculo do erro
        lista_res = lista_res + [abs(res - constantes[j])]
        i = 0
        res = 0
        j += 1
        if j == len(solucao):
            break
    if max(lista_res) > precisao:
        return False
    elif max(lista_res) < precisao:
        return True

def retira_zeros_diagonal(coeficientes, termo_indp):
    """
    Função retira_zeros_diagonal: tuplo × tuplo → tuplo × tuplo
    
    A funçao retorna uma nova matriz com as mesmas linhas que
    a de entrada, mas com estas reordenadas de forma a não 
    existirem valores 0 na diagonal.
    """
    lista_coeficientes = []
    for e in coeficientes:
        lista_coeficientes = lista_coeficientes + [list(e)]
    lista_term_indp = list(termo_indp)
    i = 0
    j = 0
    while i < len(lista_coeficientes):
        if lista_coeficientes[i][i] == 0:
            while j < len(lista_coeficientes):
                # Caso a linha i tenha um 0 na diagonal trocar esta com a
                # primeira linha j que, procurada desde o início, não tenha
                # zero na posição i e não haja um 0 na coluna j.
                if lista_coeficientes[i][i] == 0 and lista_coeficientes[j][i] != 0:
                    lista_coeficientes[j], lista_coeficientes[i] =\
                    lista_coeficientes[i], lista_coeficientes[j]
                    lista_term_indp[j], lista_term_indp[i] = lista_term_indp[i], lista_term_indp[j]
                    j = 0
                    break
                else:
                    j +=1
            j = 0
        else:
            i += 1
    lista_final = [lista_coeficientes] + [lista_term_indp]
    i = 0
    while i < len(lista_final[0]):
        lista_final[0][i] = tuple(lista_final[0][i])
        i += 1
    return tuple(map(tuple, lista_final))

def eh_diagonal_dominante(matriz):
    """
    Função eh_diagonal_dominante: tuplo → booleano
    
    Esta função retorna o valor booleano correspondente ao facto da
    matriz ter diagonal dominante ou não.
    """
    total = 0
    diag = 0
    i = 0
    j = 0
    for e in matriz:
        while i < len(e):
            total = total + abs(e[i])
            i += 1
        diag = abs(e[j])
        i = 0
        if (total - diag) > diag:
            return False
        else:
            j +=1
            total = 0
    return True

def verifica_resolve_sistema(matriz, constantes, precisao):
    """
    Função verifica_resolve_sistema: tuplo × tuplo × real → booleano

    Esta função é uma função auxiliar para verificar
    os argumentos na função obtem_resultado_eleicoes.
    """
    if type(matriz) != tuple or type(constantes) != tuple or not isinstance\
        (precisao, (int, float)) or precisao <= 0:
        raise ValueError("resolve_sistema: argumentos invalidos")
    if len(matriz) != len(constantes):
        raise ValueError("resolve_sistema: argumentos invalidos")   
    for linha in matriz:
        if type(linha) != tuple or len(linha) != len(matriz) or len(matriz) < 1:
             raise ValueError("resolve_sistema: argumentos invalidos")
        for coluna in linha:
            if not isinstance(coluna, (int, float)):
                raise ValueError("resolve_sistema: argumentos invalidos")
    for coluna in constantes:
        if not isinstance(coluna, (int, float)):
            raise ValueError("resolve_sistema: argumentos invalidos")

def resolve_sistema(matriz, constantes, precisao):
    """
    Função resolve_sistema: tuplo × tuplo × real → tuplo
    
    Esta função retorna a solução do sistema de equações
    de entrada aplicando o método de Jacobi tendo em conta
    uma certa precisão.
    """
    verifica_resolve_sistema(matriz, constantes, precisao)
    solucao = [0] * len(constantes)
    solucao_anterior = solucao.copy()
    matriz, constantes = retira_zeros_diagonal(matriz, constantes)
    if not (eh_diagonal_dominante(matriz)):
        raise ValueError("resolve_sistema: matriz nao diagonal dominante")

    while not verifica_convergencia(matriz, constantes, solucao, precisao):
        i = 0
        while i < len(matriz):       #iterar pelas linhas
            solucao[i] = solucao_anterior[i] + (constantes[i]\
            - produto_interno(matriz[i], solucao_anterior))/matriz[i][i]
            i += 1
        solucao_anterior = solucao.copy()
    return tuple(solucao)