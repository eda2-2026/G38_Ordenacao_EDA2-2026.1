# Organizador de Pelada

Conteúdo da Disciplina: Algoritmos de Ordenação

## Alunos
|Matrícula | Aluno |
| 231039178  |  Pedro Felipe Silva Vargas |

## Sobre
O projeto é um sistema de gerenciamento de jogadores para peladas semanais de futebol, agora focado na aplicação e comparação de **Algoritmos de Ordenação**. O projeto conta com uma API backend em Python (FastAPI) e uma interface Web interativa (HTML/JS/CSS puro).

Para demonstrar empiricamente a diferença de complexidade assintótica, o sistema foi populado com **2.500 jogadores únicos**. A aplicação permite randomizar a lista e ordená-la instantaneamente de forma simultânea, medindo o tempo de execução (em segundos) de três algoritmos clássicos:

- **Bubble Sort**: Algoritmo de ordenação simples com complexidade $O(N^2)$, demonstrando uma execução substancialmente mais lenta em listas grandes.
- **Merge Sort**: Algoritmo eficiente baseado em divisão e conquista, com complexidade $O(N \log N)$ em todos os casos.
- **Quick Sort**: Algoritmo eficiente também baseado em divisão e conquista, com complexidade média $O(N \log N)$, geralmente sendo o mais rápido na prática.

Além da ordenação, o sistema mantém as funcionalidades de adicionar novos jogadores, buscar por nome e alterar o status de pagamento.

## Vídeo

*(Insira o link do vídeo aqui)*

## Screenshots

*(Você pode adicionar as imagens da nova interface web na pasta `imagens/` e referenciá-las aqui, ex: `![Dashboard](imagens/dashboard.png)`)*

## Instalação
Linguagem: Python 3
Framework: FastAPI

Pré-requisitos:
- Python 3.6 ou superior instalado

Crie e ative um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Linux/Mac
# ou no Windows: venv\Scripts\activate
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

Execute o servidor da aplicação com:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Em seguida, abra o seu navegador e acesse:
**http://127.0.0.1:8000**

A interface web apresentará opções para:
1. **Adicionar Jogador**
2. **Buscar Jogador**
3. **Randomizar Lista** (embaralha a lista atual em memória)
4. **Comparar Algoritmos** (ordena a lista por Nome, Posição ou Status usando os 3 algoritmos simultaneamente e exibe o tempo comparativo)
5. **Alterar Status** (modifica diretamente na tabela)
