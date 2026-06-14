# TeoComp-Trabalho_Pratico — Parser do jogo Super Trunfo (trabalho)

Descrição
-
Este diretório contém um analisador léxico e sintático implementado com PLY (Python Lex/Yacc) para processar uma representação textual simplificada de partidas do jogo "Super Trunfo". O parser valida a sintaxe e semântica das cartas, compara atributos ativados em cada rodada e gera um relatório com o placar e o histórico das rodadas.

Estrutura relevante
-
- `parser/lexer_trunfo.py`: analisador léxico (tokens e regras de tokenização).
- `parser/parser_trunfo.py`: gramática, regras semânticas, comparação de cartas e função `parser_trunfo(cadeia_jogo)`.
- `parser/main.py`: ponto de entrada para execução via linha de comando; lê um arquivo de entrada e grava o resultado em um arquivo de saída.
- `parser/desenho_dog.py`: arte ASCII adicionada ao final da saída.
- `data/`: exemplos de entrada (`input_*.txt`) e saída (`output_*.txt`).

Requisitos
-
- Python 3.8+ (testado com Python 3.x)
- Biblioteca PLY

Instalação (Linux)
-
1. Abra um terminal e navegue até a raiz do repositório.
2. Instale o PLY se ainda não tiver:

```bash
python3 -m pip install --user ply
```

Execução (Linux)
-
Execute o analisador apontando para um arquivo de entrada em `data/`. Exemplo:

```bash
python3 parser/main.py data/input_0.txt
```

Isso criará (ou sobrescreverá) o arquivo `data/output_0.txt` com o resultado do processamento.

Formato da entrada
-
A cadeia de entrada representa uma sequência de rodadas centradas no símbolo `#` (pivô). Cada carta tem 5 atributos no formato:

```
[A, B, C, D, E]
```

Um dos cinco valores deve estar entre parênteses para indicar qual atributo foi ativado naquela carta (por exemplo, `(10)`). Os parênteses determinam o atributo comparado nessa rodada.

Regras importantes de formatação (a gramática é sensível a espaços em posições específicas):

- Os separadores internos de valores na carta devem seguir o padrão `, ` (vírgula seguido de espaço).
- Deve haver um espaço simples entre cada carta e o símbolo `#` (pivô):

Exemplo mínimo de uma rodada (válido):

```
[(10), 20, 30, 2, 5] # [12, (18), 25, 3, 4]
```

Significado do exemplo
-
- A primeira carta ativa o atributo `Comprimento` (valor 10).
- A segunda carta ativa o atributo `Peso` (valor 18).
- O parser compara apenas o atributo que está entre parênteses em cada carta da rodada correspondente.

Saída esperada
-
O programa produz um texto com:

- `CADEIA ACEITA` (ou `CADEIA REJEITADA` + motivo)
- Placar final (J1 x J2)
- Histórico das rodadas (quem venceu cada rodada ou empate)
- Uma arte ASCII (`DESENHO_DOG`) ao final

Erros comuns e mensagens
-
- Erro de Sintaxe: gerado quando a cadeia não respeita a gramática (parênteses/ vírgulas/ espaços faltando ou token inesperado).
- Erro semântico (`ValueError`): gerado quando um atributo está fora dos limites permitidos. Limites:
	- comprimento: 1–9999
	- peso: 1–99999
	- velocidade: 1–999
	- risco: 0–9
	- agressividade: 0–9

Exemplos de uso rápido
-
1) Rodada simples (arquivo `data/input_example.txt` contendo a linha abaixo):

```
[(10), 20, 30, 2, 5] # [12, (18), 25, 3, 4]
```

2) Executar:

```bash
python3 parser/main.py data/input_example.txt
cat data/output_example.txt
```

Dicas de depuração
-
- Verifique espaços: a gramática exige espaços em pontos específicos; falta de espaço pode gerar `SyntaxError`.
- Confirme que há exatamente um par de parênteses em cada carta para marcar o atributo ativado.
- Para mensagens de erro semânticas, cheque os valores numéricos dos atributos.

Referências a arquivos do código
-
- Handler/entrada: [parser/main.py](parser/main.py)
- Gramática e execução: [parser/parser_trunfo.py](parser/parser_trunfo.py)
- Lexer: [parser/lexer_trunfo.py](parser/lexer_trunfo.py)

