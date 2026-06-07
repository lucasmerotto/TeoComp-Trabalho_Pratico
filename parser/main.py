import sys
import os # sys e os para manipulação de arquivos (input e output)
from parser_trunfo import parser_trunfo

# ==============================================
# MAIN
# ==============================================
if __name__ == "__main__":
    if len(sys.argv) < 2: # len(sys.argv) é o número de argumentos da chamada do programa
        print("Não passou arquivo de entrada")
        print("Exemplo de chamada correta: python parser/super_trunfo.py data/input_0.txt\n")
        sys.exit(1)

     # Se usuário passou argumento do arquivo de entrada, salva como nome do caminho
    caminho_entrada = sys.argv[1]
    
     # Se o caminho da entrada não exise, é inválido
    if not os.path.exists(caminho_entrada):
        print(f"Erro: arquivo {caminho_entrada} não encontrado.")
        sys.exit(1)
    
     # Remove espaços brancos inúteis do início e final da cadeia
    with open(caminho_entrada, 'r', encoding='utf-8') as arquivo_entrada:
        cadeia_jogo = arquivo_entrada.read().strip()

    resultado_jogo = parser_trunfo(cadeia_jogo)

    # Escrita da saída no arquivo correspondente
    diretorio, nome_arquivo = os.path.split(caminho_entrada)
    nome_saida = nome_arquivo.replace('input', 'output')
    caminho_saida = os.path.join(diretorio, nome_saida)

    with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(resultado_jogo)