def cria_gerador(bits, estado):
    """
    Função cria_gerador: int × int → gerador (dicionário)
    
    Esta função cria um gerador.
    """
    if not type(bits) == int or not (bits == 32 or bits == 64)\
    or type(estado) != int or estado <= 0:
        raise ValueError("cria_gerador: argumentos invalidos")
    if bits == 32 and estado > 2**32:
        raise ValueError("cria_gerador: argumentos invalidos")
    if bits == 64 and estado > 2**64:
        raise ValueError("cria_gerador: argumentos invalidos")
    return {"bits": bits, "estado": estado}

def cria_copia_gerador(ger):
    """
    Função cria_copia_gerador: gerador → gerador    

    Esta função cria uma cópia do gerador recebido.
    """
    return dict(ger)

def obtem_estado(ger):
    """
    Função obtem_estado: gerador → int

    Esta função devolve o estado do gerador.
    """
    return ger["estado"]

def define_estado(ger, estado):
    """
    Função define_estado: gerador × int → int
    
    Esta função altera o estado do gerador.
    """
    ger["estado"] = estado
    return estado

def atualiza_estado(ger):
    """
    Função atualiza_estado: gerador → int
    
    Esta função atualiza o estado do gerador de acordo com 
    o algoritmo xorshift de geração de números pseudoaleatórios.
    """
    if ger["bits"] == 32:
        ger["estado"] ^= ( ger["estado"] << 13) & 0xFFFFFFFF
        ger["estado"] ^= ( ger["estado"] >> 17) & 0xFFFFFFFF
        ger["estado"] ^= ( ger["estado"] << 5) & 0xFFFFFFFF
    elif ger["bits"] == 64:
        ger["estado"] ^= ( ger["estado"] << 13) & 0xFFFFFFFFFFFFFFFF
        ger["estado"] ^= ( ger["estado"] >> 7) & 0xFFFFFFFFFFFFFFFF
        ger["estado"] ^= ( ger["estado"] << 17) & 0xFFFFFFFFFFFFFFFF
    return ger["estado"]

def eh_gerador(arg):
    """
    Função eh_gerador: universal → booleano
    
    Esta função verifica se um dado argumento é
    ou não um gerador.
    """
    return isinstance(arg, dict) and "bits" in arg and "estado"\
    in arg and (arg["bits"] == 32 or arg["bits"] == 64) and\
    isinstance(arg["estado"], int) and arg["estado"] > 0

def geradores_iguais(ger1, ger2):
    """
    Função geradores_iguais: gerador × gerador → booleano
    
    Esta função verifica se os geradores dados são ou não iguais.
    """
    return eh_gerador(ger1) and eh_gerador(ger2) and ger1 == ger2

def gerador_para_str(ger):
    """"
    Função gerador_para_str: gerador → str
    
    Esta função devolve a cadeia de carateres que 
    representa o gerador dado.
    """
    if ger["bits"] == 32:
        return f"xorshift32(s={obtem_estado(ger)})"
    return f"xorshift64(s={obtem_estado(ger)})"

def gera_numero_aleatorio(ger, n):
    """
    Função gera_numero_aleatorio: gerador × int → int
    
    Esta função gera um número aleatório através do gerador dado.
    """
    atualiza_estado(ger)
    return 1 + obtem_estado(ger)%n

def gera_carater_aleatorio(ger, c):
    """
    Função gera_carater_aleatorio: gerador × str → str
    
    Esta função gera um caráter aleatório através do gerador dado.
    """
    atualiza_estado(ger)
    entre_A_e_c = ord(c) - ord("A") + 1
    return chr(ord("A") + obtem_estado(ger)%entre_A_e_c)

def cria_coordenada(col, lin):
    """
    Função cria_coordenada: str × int → coordenada (tuplo)
    
    Esta função cria uma coordenada.
    """
    if not isinstance(col, str) or not isinstance(lin, int) or\
    not len(col) == 1 or not (ord("A") <= ord(col) <= ord("Z"))\
    or not (1 <= lin <= 99):
        raise ValueError("cria_coordenada: argumentos invalidos")
    return (col, lin)

def obtem_coluna(coord):
    """
    Função obtem_coluna: coordenada → str
    
    Esta função devolve a coluna a que corresponde a 
    coordenada fornecida.
    """
    return coord[0]

def obtem_linha(coord):
    """
    Função obtem_linha: coordenada → int
    
    Esta função devolve a linha a que corresponde a 
    coordenada fornecida.
    """
    return coord[1]

def eh_coordenada(arg):
    """
    Função eh_coordenada: universal → booleano
    
    Esta função verifica se um dado argumento é
    ou não uma coordenada.
    """
    return isinstance(arg, tuple) and isinstance(arg[0], str) and\
    isinstance(arg[1], int) and len(arg[0]) == 1 and \
    (ord("A") <= ord(arg[0]) <= ord("Z")) and (1 <= arg[1] <= 99)

def coordenadas_iguais(coord1, coord2):
    """
    Função coordenadas_iguais: coordenada × coordenada → booleano
    
    Esta função verifica se as coordenadas dadas são ou não iguais.
    """
    return eh_coordenada(coord1) and eh_coordenada(coord2) and coord1 == coord2

def coordenada_para_str(coord):
    """
    Função coordenada_para_str: coordenada → str
    
    Esta função devolve a cadeia de carateres que representa a 
    coordenada dada.
    """
    def int_to_str(coord_int):
        """
        Função int_to_str: coordenada → str
        
        Esta função é uma função auxiliar que devolve a cadeia de 
        carateres que representa a coordenada dada respeitando a 
        forma como deve ser apresentada.
        """
        return "0" + str(coord_int) if coord_int < 10 else str(coord_int)
    return obtem_coluna(coord) + int_to_str(obtem_linha(coord))

def str_para_coordenada(string):
    """
    Função str_para_coordenada: str → coordenada
    
    Esta função devolve a coordenada reapresentada pelo seu argumento.
    """
    return cria_coordenada(string[0], int(string[1:]))

def obtem_coordenadas_vizinhas(coord):
    """
    Função obtem_coordenadas_vizinhas: coordenada → tuplo
    
    Esta função devolve o tuplo com as coordenadas vizinhas às da
    coordenada fornecida.
    """
    res = []
    i = -1
    while i < 2:
        if ord("A") <= (ord(obtem_coluna(coord)) + i) <= ord("Z") and \
        1 <= obtem_linha(coord) - 1 <= 99:
            res += [cria_coordenada(chr((ord(obtem_coluna(coord)) + i)), \
            obtem_linha(coord) - 1)]
            i += 1
        else:
            i += 1
    if ord("A") <= (ord(obtem_coluna(coord)) + 1) <= ord("Z") and \
    1 <= obtem_linha(coord) <= 99:
        res += [cria_coordenada(chr((ord(obtem_coluna(coord)) + 1)), \
        obtem_linha(coord))]
    i = 1
    while i > -2:
        if ord("A") <= (ord(obtem_coluna(coord)) + i) <= ord("Z") and \
        1 <= obtem_linha(coord) + 1 <= 99:
            res += [cria_coordenada(chr((ord(obtem_coluna(coord)) + i)), \
            obtem_linha(coord) + 1)]
            i -= 1
        else:
            i -= 1
    if ord("A") <= (ord(obtem_coluna(coord)) - 1) <= ord("Z") and \
    1 <= obtem_linha(coord) <= 99:
        res += [cria_coordenada(chr((ord(obtem_coluna(coord)) - 1)), \
        obtem_linha(coord))]
    return tuple(res)

def obtem_coordenada_aleatoria(coord_max, ger):
    """
    Função obtem_coordenada_aleatoria: coordenada × gerador → coordenada
    
    Esta função devolve uma coordenada aleatória gerada através do gerador
    fornecido.
    """
    return cria_coordenada(gera_carater_aleatorio(ger, obtem_coluna(coord_max)),\
            gera_numero_aleatorio(ger, obtem_linha(coord_max)))

def cria_parcela():
    """
    Função cria_parcela: {} → parcela (lista)
    
    Esta função devolve uma parcela tapada sem mina escondida.
    """
    return ["Tapada", "Sem Mina"]

def cria_copia_parcela(parcela):
    """
    Função cria_copia_parcela: parcela → parcela
    
    Esta função devolve uma nova cópia da parcela dada.
    """
    return parcela.copy()

def limpa_parcela(parcela):
    """
    Função limpa_parcela: parcela → parcela
    
    Esta função limpa a parcela dada.
    """
    parcela[0] = "Limpa"
    return parcela

def marca_parcela(parcela):
    """
    Função marca_parcela: parcela → parcela
    
    Esta função marca a parcela dada.
    """
    parcela[0] = "Marcada"
    return parcela

def desmarca_parcela(parcela):
    """
    Função desmarca_parcela: parcela → parcela
    
    Esta função desmarca a parcela dada.
    """
    parcela[0] = "Tapada"
    return parcela

def esconde_mina(parcela):
    """
    Função esconde_mina: parcela → parcela
    
    Esta função esconde uma mina na parcela dada.
    """
    parcela[1] = "Com Mina"
    return parcela

def eh_parcela(arg):
    """
    Função eh_parcela: universal → booleano
    
    Esta função verifica se um dado argumento é
    ou não uma parcela.
    """
    return isinstance(arg, list) and len(arg) == 2 and\
    (arg[0] == "Tapada" or arg[0] == "Marcada" or \
    arg[0] == "Limpa") and (arg[1] == "Sem Mina" or arg[1] == "Com Mina")

def eh_parcela_tapada(parcela):
    """
    Função eh_parcela_tapada: parcela → booleano
    
    Esta função verifica se a parcela dada é
    ou não uma parcela tapada.
    """
    return eh_parcela(parcela) and parcela[0] == "Tapada"

def eh_parcela_marcada(parcela):
    """
    Função eh_parcela_marcada: parcela → booleano
    
    Esta função verifica se a parcela dada é
    ou não uma parcela marcada.
    """
    return eh_parcela(parcela) and parcela[0] == "Marcada"

def eh_parcela_limpa(parcela):
    """
    Função eh_parcela_limpa: parcela → booleano
    
    Esta função verifica se a parcela dada é
    ou não uma parcela limpa.
    """
    return eh_parcela(parcela) and parcela[0] == "Limpa"

def eh_parcela_minada(parcela):
    """
    Função eh_parcela_minada: parcela → booleano
    
    Esta função verifica se a parcela dada é
    ou não uma parcela minada.
    """
    return eh_parcela(parcela) and parcela[1] == "Com Mina"

def parcelas_iguais(parcela1, parcela2):
    """
    Função parcelas_iguais: parcela → booleano
    
    Esta função verifica se as parcelas dadas são
    ou não iguais.
    """
    return eh_parcela(parcela1) and eh_parcela(parcela2) and\
    parcela1 == parcela2

def parcela_para_str(parcela):
    """
    Função parcela_para_str: parcela → str
    
    Esta função devolve a cadeia de caracteres que representa a parcela
    em função do seu estado.
    """
    if eh_parcela_tapada(parcela):
        return "#"
    if eh_parcela_marcada(parcela):
        return "@"
    if eh_parcela_limpa(parcela) and not eh_parcela_minada(parcela):
        return "?"
    if eh_parcela_limpa(parcela) and eh_parcela_minada(parcela):
        return "X"

def alterna_bandeira(parcela):
    """
    Função alterna_bandeira: parcela → booleano
    
    Esta função recebe uma parcela p e modifica-a destrutivamente 
    desmarcando-a se estiver marcada e marcando-a se estiver tapada.
    """
    if eh_parcela_marcada(parcela):
        desmarca_parcela(parcela)
        return True
    if eh_parcela_tapada(parcela):
        marca_parcela(parcela)
        return True
    return False
    
def cria_campo(col, lin):
    """
    Função cria_campo: str × int → campo (lista)
    
    Esta função cria um campo de jogo.
    """
    if not isinstance(col, str) or not isinstance(lin, int)\
    or not len(col) == 1 or not(ord("A") <= ord(col) <= ord("Z"))\
    or not (1 <= lin <= 99):
        raise ValueError("cria_campo: argumentos invalidos")
    campo = []
    i = 1
    ordem_letra = ord("A")
    while i <= lin:
        while ordem_letra <= ord(col):
            campo += [[cria_coordenada(chr(ordem_letra), i), cria_parcela()]]
            ordem_letra += 1
        ordem_letra = ord("A")
        i += 1
    return campo

def cria_copia_campo(campo):
    """
    Função cria_copia_campo: campo → campo
    
    Esta função recebe um campo e devolve uma nova cópia do campo.
    """
    res = []
    for conjunto in campo:
        res += [[conjunto[0], cria_copia_parcela(conjunto[1])]]
    return res

def obtem_ultima_coluna(campo):
    """
    Função obtem_ultima_coluna: campo → str
    
    Esta função devolve a ultima coluna do campo.
    """
    return obtem_coluna(campo[-1][0])

def obtem_ultima_linha(campo):
    """
    Função obtem_ultima_linha: campo → str
    
    Esta função devolve a ultima linha do campo.
    """
    return obtem_linha(campo[-1][0])

def obtem_parcela(campo, coord):
    """
    Função obtem_parcela: campo × coordenada → parcela

    Esta função devolve a parcela correspondente à coordenada dada
    de um certo campo.
    """
    i = 0
    for parcela in campo:
        if parcela[0] != coord:
            i += 1
        else:
            break
    return campo[i][1]

def obtem_coordenadas(campo, estado):
    """
    Função obtem_coordenadas: campo × str → tuplo
    
    Esta função devolve o tuplo formado pelas coordenadas ordenadas
    em ordem ascendente da esquerda para a direita e de cima para baixo
    das parcelas dependendo do valor do estado dado.
    """
    res = []
    ult_col = obtem_ultima_coluna(campo)
    ult_lin = obtem_ultima_linha(campo)
    i = ord("A")
    j = 1
    cord = ""
    while j <= ult_lin:
        while i <= ord(ult_col):
            cord = cria_coordenada(chr(i), j)
            if estado == "limpas" and \
            eh_parcela_limpa(obtem_parcela(campo, cord)):
                res += (cord,)
            elif estado == "marcadas" and \
            eh_parcela_marcada(obtem_parcela(campo, cord)):
                res += (cord,)
            elif estado == "tapadas" and \
            eh_parcela_tapada(obtem_parcela(campo, cord)):
                res += (cord,)
            elif estado == "minadas" and \
            eh_parcela_minada(obtem_parcela(campo, cord)):
                res += (cord,)
            i += 1
        i = ord("A")
        j += 1
    return tuple(res)

def obtem_numero_minas_vizinhas(campo, coord):
    """
    Função obtem_numero_minas_vizinhas: campo × coordenada → int
    
    Esta função devolve o numero de minas vizinhas a uma certa coordenada
    de um dado campo.
    """
    res = 0
    cords_vizinhas = obtem_coordenadas_vizinhas(coord)
    for cord_viz in cords_vizinhas:
        if eh_coordenada_do_campo(campo, cord_viz) and \
        eh_parcela_minada(obtem_parcela(campo, cord_viz)):
            res += 1
    return res

def eh_campo(arg):
    """
    Função eh_campo: universal → booleano
    
    Esta função verifica se um dado argumento é ou não
    um campo.
    """
    if not isinstance(arg, list) or len(arg) == 0:
        return False
    for parcela in arg:
        return isinstance(arg, list) and isinstance(parcela, list) and\
        eh_coordenada(parcela[0]) and eh_parcela(parcela[1])

def eh_coordenada_do_campo(campo, coord):
    """
    Função eh_coordenada_do_campo: campo × coordenada → booleano
    
    Esta função verifica se uma dada coordenada é ou não coordenada
    de um dado campo.
    """
    for conjunto in campo:
        if coord in conjunto:
            return True
    return False

def campos_iguais(campo1, campo2):
    """
    Função campos_iguais: campo × campo → booleano
    
    Esta função verifica se os campos dados são ou não iguais.
    """
    if eh_campo(campo1) and eh_campo(campo2) and \
    obtem_ultima_coluna(campo1) == obtem_ultima_coluna(campo2) and \
    obtem_ultima_linha(campo1) == obtem_ultima_linha(campo2):
        for cord1 in campo1:
            for cord2 in campo2:
                if cord1[0] == cord2[0]:
                    if not parcelas_iguais(obtem_parcela(campo1, cord1[0]),\
                    obtem_parcela(campo2, cord2[0])):
                        return False
                    break
        return True
    return False

def campo_para_str(campo):
    """
    Função campo_para_str: campo → str
    
    Esta função devolve uma cadeia de caracteres que representa o campo
    de minas.
    """
    ultima_col = obtem_ultima_coluna(campo)
    ultima_lin = obtem_ultima_linha(campo)
    letras = ""
    i = ord("A")
    # Obter a string correspondente às colunas
    while i <= ord(ultima_col):
        letras = letras + chr(i)
        i += 1
    parte_cima = "   " + letras + "\n" + "  +" + "-" * len(letras) + "+\n"
    i = 1 # Contador para fazer os números correspondentes às linhas.
    j = 0 # Contador para saber de quantas em quantas parcelas parar.
    parte_meio = ""
    str_parcelas = ""
    for conjuntos in campo:
        # Caso seja uma parcela com minas vizinhas, colocar o número.
        if obtem_numero_minas_vizinhas(campo, conjuntos[0]) >= 1 and \
        not eh_parcela_minada(conjuntos[1]) and eh_parcela_limpa(conjuntos[1]):
            str_parcelas = str_parcelas + \
            str(obtem_numero_minas_vizinhas(campo, conjuntos[0]))
            j += 1
        # Caso seja uma parcela limpa.
        elif parcela_para_str(conjuntos[1]) == "?":
            str_parcelas = str_parcelas + " "
            j += 1
        else:
            str_parcelas = str_parcelas + parcela_para_str(conjuntos[1])
            j += 1
        if j == (ord(letras[-1]) - ord("A") + 1):
            num = "0" + str(i) if i < 10 else str(i)
            parte_meio = parte_meio + num + "|" + str_parcelas + "|\n"
            i += 1
            j = 0
            str_parcelas = ""
    parte_baixo = "  +" + "-" * len(letras) + "+"
    res = parte_cima + parte_meio + parte_baixo
    return res

def coloca_minas(campo, coord_orig, gerador, n_minas):
    """
    Função coloca_minas: campo × coordenada × gerador × int 7→ campo
    
    Esta função esconde n minas dentro do campo de forma aleatória
    através de um dado gerador.
    """
    cords_minas = []
    cords_vizinhas = obtem_coordenadas_vizinhas(coord_orig)
    while n_minas > 0:
        cord_aleatoria = obtem_coordenada_aleatoria(cria_coordenada\
        (obtem_ultima_coluna(campo), obtem_ultima_linha(campo)), gerador)
        # Se a coordenada não coincidir com a original ou com  
        # uma das vizinhas, adiciona.
        if cord_aleatoria not in cords_vizinhas and \
        coord_orig != cord_aleatoria and cord_aleatoria not in cords_minas:
            cords_minas += [cord_aleatoria]
            n_minas -= 1
    for coloca_minas in cords_minas:
        esconde_mina(obtem_parcela(campo, coloca_minas))
    return campo

def limpa_campo(campo, coord):
    """
    Função limpa_camp: campo × coordenada → campo
    
    Esta função limpa a parcela na coordenada fornecida e limpa
    também as parcelas das coordenadas vizinhas se o número de
    minas vizinhas dessa coordenada for 0.
    """
    if eh_coordenada_do_campo(campo, coord) and\
        eh_parcela_minada(obtem_parcela(campo, coord)):
        limpa_parcela(obtem_parcela(campo, coord))
        return campo
    if eh_coordenada_do_campo(campo, coord) and not \
        eh_parcela_minada(obtem_parcela(campo, coord)) and\
        obtem_numero_minas_vizinhas(campo, coord) != 0:
        limpa_parcela(obtem_parcela(campo, coord))
        return campo
    cords_para_limpar = []
    coordenadas_viz = obtem_coordenadas_vizinhas(coord)
    for coords in coordenadas_viz:
        if eh_coordenada_do_campo(campo, coords) and not \
        eh_parcela_minada(obtem_parcela(campo, coords)) and\
        obtem_numero_minas_vizinhas(campo, coords) == 0 and\
        not eh_parcela_marcada(obtem_parcela(campo, coords)):
            cords_para_limpar += [coords]
    cords_para_limpar_copia = []
    # O ciclo vai sendo feito até não ser adicionada nenhuma nova
    # coordenada para limpar.
    while len(cords_para_limpar) != len(cords_para_limpar_copia):
        cords_para_limpar_copia = cords_para_limpar.copy()
        for coords in cords_para_limpar:
            if eh_coordenada_do_campo(campo, coords) and \
            obtem_numero_minas_vizinhas(campo, coords) == 0:
                vizinhas = obtem_coordenadas_vizinhas(coords)
                for cord in vizinhas:
                    if eh_coordenada_do_campo(campo, cord) and cord not in\
                    cords_para_limpar and \
                    eh_parcela_tapada(obtem_parcela(campo, cord)):
                        cords_para_limpar += [cord]
    for limpar in cords_para_limpar:
        limpa_parcela(obtem_parcela(campo, limpar))
    limpa_parcela(obtem_parcela(campo, coord))
    return campo

def jogo_ganho(campo):
    """
    Função jogo_ganho: campo → booleano
    
    Esta função recebe um campo com minas e verifica se o jogo 
    já foi ganho.
    """
    return ((ord(obtem_ultima_coluna(campo)) - ord("A") + 1) * \
    obtem_ultima_linha(campo) - len(obtem_coordenadas(campo, "minadas"))) \
    == len(obtem_coordenadas(campo, "limpas"))

def turno_jogador(campo):
    """"
    Função turno_jogador: campo → booleano
    
    Esta função recebe um campo de minas e oferece ao jogador
    a opção de escolher uma ação (Limpar ou Marcar) e uma coordenada
    executando a ação dependendo da escolha na coordeanda escolhida.
    """
    escolha_L_ou_M = ""
    coord = "12345667"
    while escolha_L_ou_M != "M" and escolha_L_ou_M != "L":
        escolha_L_ou_M = input("Escolha uma ação, [L]impar ou [M]arcar:")
    while len(coord) != 3 or not isinstance(coord, str) or \
    not (ord("A") <= ord(coord[0]) <= ord(obtem_ultima_coluna(campo)))\
    or coord[1] not in map(lambda x: str(x), list(range(10))) or\
    coord[2] not in map(lambda x: str(x), list(range(10))) or not \
    (1 <= int(coord[1:3]) <= obtem_ultima_linha(campo)):
        coord = input("Escolha uma coordenada:")
    if escolha_L_ou_M == "M":
        return \
        alterna_bandeira(obtem_parcela(campo,str_para_coordenada(coord)))
    elif escolha_L_ou_M == "L":
        limpa_campo(campo, str_para_coordenada(coord))
        return \
        not eh_parcela_minada(obtem_parcela(campo, str_para_coordenada(coord)))
    
def erros_minas(ult_col, ult_lin, n_minas, bits, seed):
    """
    Função erros_minas: str × int × int × int × int → booleano
    
    Esta função verifica os erros da função minas.
    """
    if not isinstance(ult_col, str) or not isinstance(ult_lin, int)\
    or not len(ult_col) == 1 or not(ord("A") <= ord(ult_col) <= ord("Z"))\
    or not (1 <= ult_lin <= 99):
        raise ValueError("minas: argumentos invalidos")
    if not isinstance(n_minas, int) or not n_minas > 0:
        raise ValueError("minas: argumentos invalidos")
    if not type(bits) == int or not (bits == 32 or bits == 64)\
    or type(seed) != int or seed <= 0:
        raise ValueError("minas: argumentos invalidos")
    if bits == 32 and seed > 2**32:
        raise ValueError("minas: argumentos invalidos")
    if bits == 64 and seed > 2**64:
        raise ValueError("minas: argumentos invalidos")
    if (ord(ult_col) - ord("A")) * ult_lin < 12 or \
    n_minas > (ord(ult_col) - ord("A")) * ult_lin:
        raise ValueError("minas: argumentos invalidos")
    

def minas(ult_col, ult_lin, n_minas, bits, seed):
    """
    Função mina: str × int × int × int × int → booleano
    
    Esta função é a função principal que permite jogar ao jogo das minas.
    """
    erros_minas(ult_col, ult_lin, n_minas, bits, seed)
    campo = cria_campo(ult_col, ult_lin)
    gerador = cria_gerador(bits, seed)
    coord_inicial = ""
    n_marcadas = len(obtem_coordenadas(campo, "marcadas"))
    bandeiras = f"   [Bandeiras {n_marcadas}/{n_minas}]"
    while len(coord_inicial) != 3 or not isinstance(coord_inicial, str) or not\
        (ord("A") <= ord(coord_inicial[0]) <= ord(obtem_ultima_coluna(campo)))\
        or not (1 <= int(coord_inicial[1:3]) <= obtem_ultima_linha(campo)):
        print(f"{bandeiras}\n{campo_para_str(campo)}")
        coord_inicial = input("Escolha uma coordenada:")
    coloca_minas(campo,str_para_coordenada(coord_inicial), gerador, n_minas)
    limpa_campo(campo, str_para_coordenada(coord_inicial))
    print(f"{bandeiras}\n{campo_para_str(campo)}")
    while not jogo_ganho(campo):
        n_marcadas = len(obtem_coordenadas(campo, "marcadas"))
        cord_explode = ""
        cords_minadas = obtem_coordenadas(campo, "minadas")
        turno_jogador(campo)
        n_marcadas = len(obtem_coordenadas(campo, "marcadas"))
        bandeiras = f"   [Bandeiras {n_marcadas}/{n_minas}]"
        print(f"{bandeiras}\n{campo_para_str(campo)}")
        for mina in cords_minadas:
            if eh_parcela_limpa(obtem_parcela(campo, mina)):
                cord_explode = "explode"
                break
        if cord_explode == "explode":
            print("BOOOOOOOM!!!")
            break
    if jogo_ganho(campo):
        print("VITORIA!!!")  
    return jogo_ganho(campo)