import ply.lex as lex
import gradio as gr

# Definição dos tokens
tokens = (
    'NUMERO',
    'VARIAVEL',
    'OPERADOR',
    'IGUALDADE'
)

# Expressões regulares para cada token
t_ignore = ' \t'

def t_NUMERO(t):
    r'\d+'
    t.value = (t.value, int(t.value))  # (TIPO, VALOR)
    return t

def t_VARIAVEL(t):
    r'[a-zA-Z]'
    t.value = (t.value, t.value)  # (TIPO, VALOR)
    return t

def t_OPERADOR(t):
    r'[\+\-\*/]'
    operadores = {'+': 'SOMA', '-': 'SUBTRAÇÃO', '*': 'MULTIPLICAÇÃO', '/': 'DIVISÃO'}
    t.value = (t.value, operadores[t.value])  # (TIPO, VALOR)
    return t

def t_IGUALDADE(t):
    r'='
    t.value = ('IGUALDADE', 'IGUALDADE')  # (TIPO, VALOR)
    t.type = 'IGUALDADE'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

# Criando o analisador léxico
lexer = lex.lex()

# Função para analisar a equação e retornar os tokens formatados corretamente
def analisar_lexicamente(equacao):
    lexer.input(equacao)
    resultado = "TOKEN | TIPO | VALOR\n"
    resultado += "-------------------------\n"
    for tok in lexer:
        tipo, valor = tok.value
        resultado += f"{tok.value[0] if tok.type != 'IGUALDADE' else '='} | {tok.type} | {valor}\n"
    return resultado

# Criando a interface Gradio
interface = gr.Interface(
    fn=analisar_lexicamente,
    inputs=gr.Textbox(label="Digite a equação do 1º grau"),
    outputs=gr.Textbox(label="Análise Léxica"),
    title="Analisador Léxico para Equações do 1º Grau",
    description="Digite uma equação na forma ax+b=0 para ver os tokens reconhecidos.",
    submit_btn="Analisar Lexicamente",  # Nome do botão de enviar
    clear_btn="Limpar",  # Nome do botão de limpar
    allow_flagging="never"  # Remove o botão Flag
)

# Executa a interface
interface.launch()
