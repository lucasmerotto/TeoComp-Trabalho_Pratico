import ply.lex as lex

# ==============================================
# LEXER - Analisador léxico
# ==============================================
# Tupla com o nome de todos os tokens que o parser vai utilizar
tokens = (
    'LBRACKET',  # [
    'RBRACKET',  # ]
    'LPAREN',    # (
    'RPAREN',    # )
    'COMMA',     # ,
    'PIVOT',     # #
    'NUMBER',    # Sequência de algarismos
    'SPACE',     # Espaço em branco
)

# Regex para os tokens mais simples
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_COMMA    = r','
t_PIVOT    = r'\#'

# Regex para capturar um ou mais espaços em branco.
def t_SPACE(t):
    r'[ \t]+'
    return t

# Regex para capturar e converter sequências numéricas
def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

t_ignore = '' # Permite que espaços NÃO sejam ignorados

# Tratamento de erros léxicos
def t_error(t):
    raise SyntaxError(f"Erro Léxico: Caractere inválido ou inesperado '{t.value[0]}' na posição {t.lexpos}") # Mensagem impressa no arquivo de sáida

# Inicializa o motor do Lexer global do PLY
lexer = lex.lex() # Aplica as regras t_... definidas acima