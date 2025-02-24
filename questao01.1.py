import ply.lex as lex
import gradio as gr

# Definicao dos tokens
tokens = (
    'NUMERO',
    'VARIAVEL',
    'OPERADOR',
    'IGUALDADE'
)

# Expressoes regulares para cada token
t_ignore = ' \t'

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_VARIAVEL(t):
    r'[a-zA-Z]'
    return t

def t_OPERADOR(t):
    r'[\+\-\*/]'
    operadores = {'+': 'SOMA', '-': 'SUBTRAÇAO', '*': 'MULTIPLICAÇAO', '/': 'DIVISAO'}
    t.valor = operadores[t.value]  # Definindo o nome do operador
    return t

def t_IGUALDADE(t):
    r'='
    t.valor = 'igualdade'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

def analisar_lexicamente(equacao):
    lexer.input(equacao)
    
    # Criando uma lista para armazenar os tokens na tabela
    tokens_tabela = []

    for tok in lexer:
        if tok.type == "OPERADOR":
            tokens_tabela.append([tok.value, tok.type, tok.valor])  # Usa o nome do operador
        elif tok.type == "IGUALDADE":
            tokens_tabela.append(["=", tok.type, "IGUALDADE"])
        else:
            tokens_tabela.append([tok.value, tok.type, tok.value])  # O valor repete o proprio valor
        
    return tokens_tabela

# Criando a interface Gradio com saída em tabela
interface = gr.Interface(
    fn=analisar_lexicamente,
    inputs=gr.Textbox(label="Digite a equacao do 1º grau"),
    outputs=gr.DataFrame(headers=["TOKEN", "TIPO", "VALOR"]),
    title="Analisador Lexico para Equacoes do 1º Grau",
    description="Digite uma equacao na forma ax+b=0 para ver os tokens reconhecidos.",
    allow_flagging="never",  # Remove o botao "Flag"
    submit_btn="Analisar Lexicamente",  # Renomeia o botao de envio
    clear_btn="Limpar"  # Renomeia o botao de limpar
)

interface.launch()
