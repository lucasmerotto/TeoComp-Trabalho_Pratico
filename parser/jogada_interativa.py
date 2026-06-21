import os
from parser_trunfo import parser_trunfo

def coletar_carta(nome_jogador, rodada):
    print(f"\n--- CARTA DO {nome_jogador.upper()} (RODADA {rodada}) ---")
    print("Escolha qual atributo será ativado nesta rodada:")
    print("1 - Comprimento (1 a 9999)")
    print("2 - Peso (1 a 99999)")
    print("3 - Velocidade (1 a 999)")
    print("4 - Risco de Extinção (0 a 9)")
    print("5 - Agressividade (0 a 9)")
    
    while True:
        try:
            opc = int(input("Digite o número do atributo ativo: "))
            if 1 <= opc <= 5:
                break
            print("Opção inválida! Escolha entre 1 e 5.")
        except ValueError:
            print("Por favor, digite um número válido.")
    
    comp = input("Valor do Comprimento: ")
    peso = input("Valor do Peso: ")
    vel = input("Valor da Velocidade: ")
    risco = input("Valor do Risco de Extinção: ")
    agres = input("Valor da Agressividade: ")

    c = f"({comp})" if opc == 1 else comp
    p = f"({peso})" if opc == 2 else peso
    v = f"({vel})" if opc == 3 else vel
    r = f"({risco})" if opc == 4 else risco
    a = f"({agres})" if opc == 5 else agres

    # Retorna a carta formatada com os espaços estritos da gramática
    return f"[{c}, {p}, {v}, {r}, {a}]"

def main():
    print("=" * 50)
    print("      SIMULADOR MULTI-RODADAS - SUPER TRUNFO     ")
    print("=" * 50)
    
    while True:
        try:
            num_cartas = int(input("Insira o numero de cartas de cada jogador: "))
            if num_cartas > 0:
                break
            print("O número de cartas deve ser maior que 0!")
        except ValueError:
            print("Por favor, digite um número inteiro válido.")

    cartas_j1 = []
    cartas_j2 = []

    # Coleta as jogadas de cada rodada
    for i in range(1, num_cartas + 1):
        print(f"\n========== CONFIGURANDO A RODADA {i} ==========")
        print("Lembrete: Ambos os jogadores devem ativar o MESMO atributo nesta rodada!")
        carta_j1 = coletar_carta("Turma (Jogador 1)", i)
        carta_j2 = coletar_carta("Professor (Jogador 2)", i)
        
        cartas_j1.append(carta_j1)
        # Inserimos no início da lista de J2 para manter o espelhamento correto na cadeia final
        cartas_j2.insert(0, carta_j2)

    # Junta as cartas com espaços simples entre elas
    str_j1 = " ".join(cartas_j1)
    str_j2 = " ".join(cartas_j2)
    
    # Monta a cadeia linear espelhada: CartaJ1_1 CartaJ1_2 # CartaJ2_2 CartaJ2_1
    cadeia_jogo = f"{str_j1} # {str_j2}"
    
    print("\n" + "=" * 50)
    print("Cadeia estruturada enviada ao Parser:")
    print(cadeia_jogo)
    print("=" * 50)
    
    # Executa o parser original do trabalho
    resultado = parser_trunfo(cadeia_jogo)
    
    print("\nRESULTADO PROCESSADO PELO PARSER:")
    print(resultado)

if __name__ == "__main__":
    main()