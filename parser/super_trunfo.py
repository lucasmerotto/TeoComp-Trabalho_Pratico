import sys
import os
import ply.lex as lex
import ply.yacc as yacc


# =====================================================================
# 1. ESCOPO GLOBAL DO LEXER (Analisador Léxico - Versão Estrita)
# =====================================================================

# Tupla obrigatória com o nome de todos os tokens que o parser vai utilizar
tokens = (
    'LBRACKET',  # [
    'RBRACKET',  # ]
    'LPAREN',    # (
    'RPAREN',    # )
    'COMMA',     # ,
    'PIVOT',     # #
    'NUMBER',    # Sequência de dígitos numéricos
    'SPACE',     # Espaço em branco explícito (apenas onde for permitido!)
)

# Regras de expressões regulares (Regex) para os tokens literais (simples)
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_COMMA    = r','
t_PIVOT    = r'\#'

# Regra para capturar exatamente um ou mais espaços em branco.
# Agora o espaço é um token oficial do jogo.
def t_SPACE(t):
    r'[ \t]+'
    return t

# Regra em forma de função para capturar e converter sequências numéricas
def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

# MUDANÇA CRÍTICA: t_ignore agora está completamente VAZIO!
# O Python não vai ignorar absolutamente nada de forma invisível.
t_ignore = ''

# Função de tratamento de erros léxicos (Rede de segurança da linguagem)
def t_error(t):
    # Interrompe o processo na hora e avisa a função principal
    raise SyntaxError(f"Erro Léxico: Caractere inválido ou inesperado '{t.value[0]}' na posição {t.lexpos}")

# Inicialização do motor do Lexer global do PLY
lexer = lex.lex()

# =====================================================================
# 2. ESCOPO GLOBAL DO PARSER (Analisador Sintático e Semântico)
# =====================================================================

# Função auxiliar para validar as restrições numéricas da sua BNF (Análise Semântica)
# <Num_C> até 9999, <Num_P> até 99999, <Num_V> até 999, <Num_R> e <Num_A> até 9
def validar_limites(c, p, v, r, a):
    if not (1 <= c <= 9999): raise ValueError(f"Comprimento {c} fora do limite (1-9999)")
    if not (1 <= p <= 99999): raise ValueError(f"Peso {p} fora do limite (1-99999)")
    if not (1 <= v <= 999): raise ValueError(f"Velocidade {v} fora do limite (1-999)")
    if not (0 <= r <= 9): raise ValueError(f"Risco de Extinção {r} fora do limite (0-9)")
    if not (0 <= a <= 9): raise ValueError(f"Agressividade {a} fora do limite (0-9)")

# ---------------------------------------------------------------------
# REGRAS DA PARTIDA (O crescimento da Árvore)
# ---------------------------------------------------------------------

# Regra Base: O miolo da partida (apenas o símbolo '#')
def p_partida_base(p):
    '''partida : PIVOT'''
    # Retorna o estado inicial do jogo: (Pontos_J1, Pontos_J2, Histórico)
    p[0] = (0, 0, [])

# Regra Recursiva: Mapeia o balanceamento das 5 cartas possíveis.
# Note o 'SPACE' exigido estritamente entre as cartas e o miolo da partida!
def p_partida_recursiva(p):
    '''partida : carta_c SPACE partida SPACE carta_c
               | carta_p SPACE partida SPACE carta_p
               | carta_v SPACE partida SPACE carta_v
               | carta_r SPACE partida SPACE carta_r
               | carta_a SPACE partida SPACE carta_a'''
    
    carta_j1 = p[1]          # Carta da esquerda
    estado_interno = p[3]    # O miolo que já foi processado (placar anterior)
    carta_j2 = p[5]          # Carta da direita
    
    pontos_j1, pontos_j2, historico = estado_interno
    
    # Compara o valor do atributo que foi ativado nesta rodada
    valor_j1 = carta_j1['valor_rodada']
    valor_j2 = carta_j2['valor_rodada']
    atributo = carta_j1['tipo']
    
    if valor_j1 > valor_j2:
        pontos_j1 += 1
        resultado = f"J1 venceu ({atributo}: {valor_j1} vs {valor_j2})"
    elif valor_j2 > valor_j1:
        pontos_j2 += 1
        resultado = f"J2 venceu ({atributo}: {valor_j2} vs {valor_j1})"
    else:
        resultado = f"Empate ({atributo}: {valor_j1} = {valor_j2})"
        
    # Adiciona o resultado no início da lista (pois o parser lê de dentro pra fora)
    historico.append(resultado)
    
    # Passa o placar atualizado para a próxima camada da "cebola"
    p[0] = (pontos_j1, pontos_j2, historico)

# ---------------------------------------------------------------------
# REGRAS DAS CARTAS (Sem espaços permitidos internamente!)
# ---------------------------------------------------------------------

# Carta com Comprimento escolhido
def p_carta_c(p):
    '''carta_c : LBRACKET LPAREN NUMBER RPAREN COMMA NUMBER COMMA NUMBER COMMA NUMBER COMMA NUMBER RBRACKET'''
    validar_limites(p[3], p[6], p[8], p[10], p[12])
    p[0] = {'tipo': 'Comprimento', 'valor_rodada': p[3]}

# ---------------------------------------------------------------------
# REGRAS DAS CARTAS (Com espaços estritos após as vírgulas)
# ---------------------------------------------------------------------

# Carta com Comprimento escolhido
def p_carta_c(p):
    '''carta_c : LBRACKET LPAREN NUMBER RPAREN COMMA SPACE NUMBER COMMA SPACE NUMBER COMMA SPACE NUMBER COMMA SPACE NUMBER RBRACKET'''
    # Índices: C=3, P=7, V=10, R=13, A=16
    validar_limites(p[3], p[7], p[10], p[13], p[16])
    p[0] = {'tipo': 'Comprimento', 'valor_rodada': p[3]}

# Carta com Peso escolhido
def p_carta_p(p):
    '''carta_p : LBRACKET NUMBER COMMA SPACE LPAREN NUMBER RPAREN COMMA SPACE NUMBER COMMA SPACE NUMBER COMMA SPACE NUMBER RBRACKET'''
    # Índices: C=2, P=6, V=10, R=13, A=16
    validar_limites(p[2], p[6], p[10], p[13], p[16])
    p[0] = {'tipo': 'Peso', 'valor_rodada': p[6]}

# Carta com Velocidade escolhida
def p_carta_v(p):
    '''carta_v : LBRACKET NUMBER COMMA SPACE NUMBER COMMA SPACE LPAREN NUMBER RPAREN COMMA SPACE NUMBER COMMA SPACE NUMBER RBRACKET'''
    # Índices: C=2, P=5, V=9, R=13, A=16
    validar_limites(p[2], p[5], p[9], p[13], p[16])
    p[0] = {'tipo': 'Velocidade', 'valor_rodada': p[9]}

# Carta com Risco de Extinção escolhido
def p_carta_r(p):
    '''carta_r : LBRACKET NUMBER COMMA SPACE NUMBER COMMA SPACE NUMBER COMMA SPACE LPAREN NUMBER RPAREN COMMA SPACE NUMBER RBRACKET'''
    # Índices: C=2, P=5, V=8, R=12, A=16
    validar_limites(p[2], p[5], p[8], p[12], p[16])
    p[0] = {'tipo': 'Risco', 'valor_rodada': p[12]}

# Carta com Agressividade escolhida
def p_carta_a(p):
    '''carta_a : LBRACKET NUMBER COMMA SPACE NUMBER COMMA SPACE NUMBER COMMA SPACE NUMBER COMMA SPACE LPAREN NUMBER RPAREN RBRACKET'''
    # Índices: C=2, P=5, V=8, R=11, A=15
    validar_limites(p[2], p[5], p[8], p[11], p[15])
    p[0] = {'tipo': 'Agressividade', 'valor_rodada': p[15]}

# ---------------------------------------------------------------------
# TRATAMENTO DE ERROS DO PARSER
# ---------------------------------------------------------------------

def p_error(p):
    if p:
        # Se achou um token que quebra a regra (ex: um SPACE onde não devia, ou atributos desbalanceados)
        raise SyntaxError(f"Erro de Sintaxe. Token inesperado: '{p.value}' (Tipo: {p.type}) na posição {p.lexpos}.")
    else:
        # Se a string acabou no meio de uma carta
        raise SyntaxError("Erro de Sintaxe. Fim de arquivo inesperado. A cadeia está incompleta.")

# Inicializa o motor do Parser
parser = yacc.yacc()


# =====================================================================
# 3. FUNÇÃO PRINCIPAL DE ORQUESTRAÇÃO
# =====================================================================

def parser_trunfo(cadeia_jogo):
    try:
        # Chama o motor sintático, que por baixo dos panos consome os tokens do Lexer
        resultado = parser.parse(cadeia_jogo)
        
        # Se o PLY retornar None sem disparar erro, a cadeia era completamente vazia
        if not resultado:
            return "CADEIA REJEITADA\nMotivo: Arquivo vazio ou erro fatal não capturado."
            
        pontos_j1, pontos_j2, historico = resultado
        
        # Montagem da string de saída de sucesso
        saida = "CADEIA ACEITA\n"
        saida += f"Placar Final: J1 {pontos_j1} x {pontos_j2} J2\n"
        saida += "-" * 30 + "\n"
        saida += "Histórico das Rodadas:\n"
        
        # Como o histórico foi montado de dentro para fora, os índices batem certinho
        for i, jogada in enumerate(historico, 1):
            saida += f"Rodada {i}: {jogada}\n"
            
        return saida

    except SyntaxError as e:
        # Captura erros estruturais (ex: faltou espaço, chaves desbalanceadas, faltou vírgula)
        return f"CADEIA REJEITADA\nMotivo: {str(e)}"
        
    except ValueError as e:
        # Captura erros semânticos (ex: Agressividade > 9, Comprimento negativo)
        return f"CADEIA REJEITADA\nMotivo: Erro Semântico - {str(e)}"
        
    except Exception as e:
        # Rede de segurança para qualquer outro problema inesperado do Python
        return f"CADEIA REJEITADA\nMotivo: Erro interno - {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) < 2: # argv é o número de argumentos da chamada do programa. Ex: em "python parser/super_trunfo.py data/input_0.txt", argv == 2
        print("Não passou arquivo de entrada")
        print("Exemplo de chamada correta: python parser/super_trunfo.py data/input_0.txt\n")
        sys.exit(1)

    caminho_entrada = sys.argv[1] # Se usuário passou argumento do arquivo de entrada, salva como nome do caminho
    
    if not os.path.exists(caminho_entrada): # Se o caminho da entrada não exise, é inválido
        print(f"Erro: arquivo {caminho_entrada} não encontrado.")
        sys.exit(1)
    
    with open(caminho_entrada, 'r', encoding='utf-8') as arquivo_entrada:
        cadeia_jogo = arquivo_entrada.read().strip() # Remove espaços brancos inúteis do início e final da cadeia

    resultado_jogo = parser_trunfo(cadeia_jogo) # Essa função interpreta a cadeia do jogo e retorna o string a ser escrita na saída

    # Escrita da saída no arquivo correspondente
    diretorio, nome_arquivo = os.path.split(caminho_entrada)
    nome_saida = nome_arquivo.replace('input', 'output')
    caminho_saida = os.path.join(diretorio, nome_saida)

    with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(resultado_jogo)