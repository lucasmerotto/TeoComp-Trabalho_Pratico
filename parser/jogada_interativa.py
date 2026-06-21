import os
from parser_trunfo import parser_trunfo

def coletar_carta(nome_jogador):
    print(f"\n--- CARTA DO {nome_jogador.upper()} ---")
    print("Escolha qual atributo será ativado nesta rodada:")
    print("1 - Comprimento (1 a 9999)")
    print("2 - Peso (1 a 99999)")
    print("3 - Velocidade (1 a 999)")
    print("4 - Risco de Extinção (0 a 9)")
    print("5 - Agressividade (0 a 9)")
    
    opc = int(input("Digite o número do atributo ativo: "))
    
    # Coleta os valores de cada atributo
    comp = input("Valor do Comprimento: ")
    peso = input("Valor do Peso: ")
    vel = input("Valor da Velocidade: ")
    risco = input("Valor do Risco de Extinção: ")
    agres = input("Valor da Agressividade: ")

    # Coloca entre parênteses apenas o atributo que foi ativado
    c = f"({comp})" if opc == 1 else comp
    p = f"({peso})" if opc == 2 else peso
    v = f"({vel})" if opc == 3 else vel
    r = f"({risco})" if opc == 4 else risco
    a = f"({agres})" if opc == 5 else agres

    # Monta a string da carta respeitando o padrão da gramática: [C, P, V, R, A]
    # Importante: a vírgula deve ser seguida de um espaço!
    return f"[{c}, {p}, {v}, {r}, {a}]"

def main():
    print("=" * 50)
    print("      SIMULADOR INTERATIVO - SUPER TRUNFO       ")
    print("=" * 50)
    
    print("\nRegra: O professor e a turma devem ativar o MESMO atributo!")
    
    # Coleta os dados dos dois jogadores
    carta_j1 = coletar_carta("Turma (Jogador 1)")
    carta_j2 = coletar_carta("Professor (Jogador 2)")
    
    # Monta a cadeia final exatamente como o parser espera: Carta1 # Carta2
    # Com os espaços estritos antes e depois do símbolo '#'
    cadeia_jogo = f"{carta_j1} # {carta_j2}"
    
    print("\nCadeia gerada para o Parser:")
    print(cadeia_jogo)
    print("-" * 50)
    
    # Executa o parser que vocês já criaram
    resultado = parser_trunfo(cadeia_jogo)
    
    # Exibe o resultado formatado na tela
    print("\nRESULTADO DO PARSER:")
    print(resultado)

if __name__ == "__main__":
    main()