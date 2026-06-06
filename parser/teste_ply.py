import ply.lex as lex

# 1. Lista de tokens que o nosso testador vai reconhecer
tokens = (
    'COLCHETE_ABRE',
    'COLCHETE_FECHA',
    'VIRGULA',
    'TRUNFO',
    'NUMERO',
)

# 2. Regras de expressões regulares para os tokens simples
t_COLCHETE_ABRE  = r'\['
t_COLCHETE_FECHA = r'\]'
t_VIRGULA        = r','
t_TRUNFO         = r'\#'

# 3. Regra para capturar números (e já converter para inteiros no Python)
def t_NUMERO(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

# Ignorar espaços em branco
t_ignore = ' \t'

# Gerenciador de erros léxicos (caracteres estranhos)
def t_error(t):
    print(f"Caractere inválido encontrado: '{t.value[0]}'")
    t.lexer.skip(1)

# 4. Construir o Lexer
lexer = lex.lex()

# 5. String de teste (Simulando uma versão simplificada das suas cartas)
texto_teste = "[120, 80] # [95, 45]"

# Alimentar o lexer com o texto
lexer.input(texto_teste)

print("--- RESULTADO DO TESTE DO LEXER ---")
# Laço para ler e printar cada token encontrado até o fim do texto
while True:
    tok = lexer.token()
    if not tok:
        break  # Fim dos tokens (Fim do texto)
    print(tok)
print("-----------------------------------")