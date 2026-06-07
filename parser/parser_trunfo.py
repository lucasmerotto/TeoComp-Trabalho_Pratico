import ply.yacc as yacc
from lexer_trunfo import tokens, lexer
from desenho_dog import DESENHO_DOG

# ==============================================
# PARSER - Analisador sintático e semântico
# ==============================================
# Validar os limites numéricos das regras de produção dos atributos (análise semântica -> ValueError)
def validar_limites(comprimento, peso, velocidade, risco, agressividade):
    if not (1 <= comprimento <= 9999): raise ValueError(f"Comprimento {comprimento} fora do limite (1-9999)")
    if not (1 <= peso <= 99999): raise ValueError(f"Peso {peso} fora do limite (1-99999)")
    if not (1 <= velocidade <= 999): raise ValueError(f"Velocidade {velocidade} fora do limite (1-999)")
    if not (0 <= risco <= 9): raise ValueError(f"Risco de Extinção {risco} fora do limite (0-9)")
    if not (0 <= agressividade <= 9): raise ValueError(f"Agressividade {agressividade} fora do limite (0-9)")


# REGRAS DA PARTIDA:
# Regra Base: O miolo da partida (apenas o símbolo '#')
def p_partida_base(p):
    '''partida : PIVOT''' # '#' vira o símbolo partida
    # Retorna o estado inicial do jogo: (Pontos_J1, Pontos_J2, Histórico)
    p[0] = (0, 0, []) # p[0] é o lado esquerdo da regra de produção

# Regra Recursiva: Mapeia o balanceamento das 5 cartas possíveis.
# Note o 'SPACE' exigido estritamente entre as cartas e o miolo da partida!
def p_partida_recursiva(p):
    '''partida : carta_c SPACE partida SPACE carta_c
               | carta_p SPACE partida SPACE carta_p
               | carta_v SPACE partida SPACE carta_v
               | carta_r SPACE partida SPACE carta_r
               | carta_a SPACE partida SPACE carta_a''' # Recursão pelo meio como temos nas regras de produção
    
    carta_j1 = p[1]          # Carta da esquerda
    estado_interno = p[3]    # O que já foi processado (partida anterior)
    carta_j2 = p[5]          # Carta da direita
    # p[2] e p[4] são espaços e são ignorados
    
    pontos_j1, pontos_j2, historico = estado_interno # Pontuações e histórico anteriores
    
    # Compara o valor do atributo que foi ativado nesta rodada (definido em um dicionário em p_carta_... em REGRAS DAS CARTAS)
    valor_j1 = carta_j1['valor_rodada']
    valor_j2 = carta_j2['valor_rodada'] # Pontuação
    atributo = carta_j1['tipo'] # Nome do atributo


    if valor_j1 > valor_j2:
        pontos_j1 += 1
        resultado = f"J1 venceu ({atributo}: {valor_j1} vs {valor_j2})"
    elif valor_j2 > valor_j1:
        pontos_j2 += 1
        resultado = f"J2 venceu ({atributo}: {valor_j2} vs {valor_j1})"
    else:
        resultado = f"Empate ({atributo}: {valor_j1} = {valor_j2})"
        
    historico.append(resultado)
    # historico e pontuação atualizados com a nova rodada
    
    # Atualiza recursão
    p[0] = (pontos_j1, pontos_j2, historico)


# REGRAS DAS CARTAS:
# Jogador escolheu atributo comprimento
def p_carta_comprimento(p):
    '''carta_c : LBRACKET LPAREN NUMBER RPAREN COMMA SPACE NUMBER COMMA SPACE NUMBER COMMA SPACE NUMBER COMMA SPACE NUMBER RBRACKET'''
    # Índices: comprimento=3, peso=7, velocidade=10, risco=13, agressividade=16
    validar_limites(p[3], p[7], p[10], p[13], p[16])
    p[0] = {'tipo': 'Comprimento', 'valor_rodada': p[3]}

def p_carta_peso(p):
    '''carta_p : LBRACKET NUMBER COMMA SPACE LPAREN NUMBER RPAREN COMMA SPACE NUMBER COMMA SPACE NUMBER COMMA SPACE NUMBER RBRACKET'''
    validar_limites(p[2], p[6], p[10], p[13], p[16])
    p[0] = {'tipo': 'Peso', 'valor_rodada': p[6]}

def p_carta_velocidade(p):
    '''carta_v : LBRACKET NUMBER COMMA SPACE NUMBER COMMA SPACE LPAREN NUMBER RPAREN COMMA SPACE NUMBER COMMA SPACE NUMBER RBRACKET'''
    validar_limites(p[2], p[5], p[9], p[13], p[16])
    p[0] = {'tipo': 'Velocidade', 'valor_rodada': p[9]}

def p_carta_risco(p):
    '''carta_r : LBRACKET NUMBER COMMA SPACE NUMBER COMMA SPACE NUMBER COMMA SPACE LPAREN NUMBER RPAREN COMMA SPACE NUMBER RBRACKET'''
    validar_limites(p[2], p[5], p[8], p[12], p[16])
    p[0] = {'tipo': 'Risco', 'valor_rodada': p[12]}

def p_carta_agressividade(p):
    '''carta_a : LBRACKET NUMBER COMMA SPACE NUMBER COMMA SPACE NUMBER COMMA SPACE NUMBER COMMA SPACE LPAREN NUMBER RPAREN RBRACKET'''
    validar_limites(p[2], p[5], p[8], p[11], p[15])
    p[0] = {'tipo': 'Agressividade', 'valor_rodada': p[15]}


# TRATAMENTO DE ERROS DO PARSER:
def p_error(p):
    if p:
        # Se achou um token que quebra a regra (ex: um SPACE onde não devia, ou atributos desbalanceados)
        raise SyntaxError(f"Erro de Sintaxe. Token inesperado: '{p.value}' (Tipo: {p.type}) na posição {p.lexpos}.")
    else:
        # Se a string acabou no meio de uma carta
        raise SyntaxError("Erro de Sintaxe. A cadeia está incompleta.")

# Inicializa o motor do Parser
parser = yacc.yacc()

# ==============================================
# FUNÇÃO PRINCIPAL
# ==============================================
def parser_trunfo(cadeia_jogo):
    try:
        # Chama o motor sintático que consome os tokens do Lexer
        resultado = parser.parse(cadeia_jogo)
        
        # Se o PLY retornar None sem disparar erro, a cadeia era completamente vazia
        if resultado == None:
            return "CADEIA REJEITADA\nEntrada vazia"
            
        pontos_j1, pontos_j2, historico = resultado # Resulatdo da última recursão (de dentro para fora)
        
        # Montagem da string de saída de sucesso
        saida = "CADEIA ACEITA\n"
        saida += f"Placar Final: J1 {pontos_j1} x {pontos_j2} J2\n"
        saida += "-" * 30 + "\n"
        saida += "Histórico das Rodadas:\n"
        
        for i, jogada in enumerate(historico, 1):
            saida += f"Rodada {i}: {jogada}\n" # Iteração sobre historico

        saida += DESENHO_DOG
            
        return saida

    except SyntaxError as e:
        # Erros estruturais (ex: faltou espaço, chaves desbalanceadas, faltou vírgula)
        return f"CADEIA REJEITADA\n{str(e)}"
        
    except ValueError as e:
        # Erros semânticos (ex: Agressividade > 9, Comprimento negativo)
        return f"CADEIA REJEITADA\n{str(e)}"
        
    except Exception as e:
        # Erro interno
        return f"CADEIA REJEITADA\n{str(e)}"