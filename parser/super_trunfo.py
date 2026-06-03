import sys
import os

# código/funções para o Lexer e o Parser

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

    print(f"Arquivo aberto: {caminho_entrada}")
    print(f"Cadeia de entrada: {cadeia_jogo}\n")

    # Escrita da saída no arquivo correspondente
    # Escrever 'teste' só por enquanto
    diretorio, nome_arquivo = os.path.split(caminho_entrada)
    nome_saida = nome_arquivo.replace('input', 'output')
    caminho_saida = os.path.join(diretorio, nome_saida)

    with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write("Dale Grêmio")

    print(f"Saída foi salva com sucesso em {caminho_saida}")