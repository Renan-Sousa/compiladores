import string
import json
import os

class Token:
    def __init__(self, char, type, name, line_number):
        self.char = char
        self.type = type
        self.name = name
        self.line_number = line_number

def analizadorLexico(file_path):
    estado = 0  # Estado inicial do AFD
    lexema = []  # Variável que guarda o lexema atualmente reconhecido
    tokens = []  # Vetor de tokens
    num_linha = 1  # Contador de linhas

    # Lista de palavras reservadas
    reservadas = {"fn", "main", "let", "int", "float", "char", "if", "else", "while", "println", "return"}

    # Abre o arquivo
    with open(file_path, "r") as file:
        for line in file:
            ibuf = line.rstrip('\n')
            i = 0

            while i < len(ibuf): #Para cada caractere da linha, executa as regras do AFD
                char = ibuf[i]
                
                if estado == 0:
                    if char == '"':
                        estado = 12
                    elif char == "'":
                        print(char)
                        estado = 10
                    elif char == '(':
                        token = Token(char, "LBRACKET", char, num_linha)
                        tokens.append(token)
                    elif char == ')':
                        token = Token(char, "RBRACKET", char, num_linha)
                        tokens.append(token)
                    elif char == '{':
                        token = Token(char, "LBRACE", char, num_linha)
                        tokens.append(token)
                    elif char == '}':
                        token = Token(char, "RBRACE", char, num_linha)
                        tokens.append(token)
                    elif char == ':':
                        token = Token(char, "COLON", char, num_linha)
                        tokens.append(token)
                    elif char == ',':
                        token = Token(char, "COMMA", char, num_linha)
                        tokens.append(token)
                    elif char == ';':
                        token = Token(char, "SEMICOLON", char, num_linha)
                        tokens.append(token)
                    elif char == '+':
                        token = Token(char, "PLUS", char, num_linha)
                        tokens.append(token)
                    elif char == '*':
                        token = Token(char, "MULT", char, num_linha)
                        tokens.append(token)
                    elif char == '/':
                        token = Token(char, "DIV", char, num_linha)
                        tokens.append(token)
                    
                    elif char == '=':
                        estado = 1
                    
                    elif char == '!':
                        estado = 2
                    
                    elif char == '>':
                        estado = 3
                    
                    elif char == '<':
                        estado = 4

                    elif char == '-':
                        estado = 5

                    elif char in string.digits:
                        lexema.append(char)
                        estado = 6

                    elif char in string.ascii_letters:
                        lexema.append(char)
                        estado = 9

                elif estado == 1:
                    if char == "=":
                        token = Token(char, "EQ", "==", num_linha)
                        tokens.append(token)
                        estado = 0
                    else:
                        token = Token(char, "ASSIGN", "=", num_linha)
                        tokens.append(token)
                        estado = 0
                        i-=1

                elif estado == 2:
                    if char == '=':
                        token = Token(char,"NE", "!=", num_linha)
                        tokens.append(token)
                        estado = 0
                
                elif estado == 3:
                    if char == '=':
                        token = Token(char, "GE", ">=", num_linha)
                        tokens.append(token)
                        estado = 0
                    else:
                        token = Token(char, "GT", ">", num_linha)
                        tokens.append(token)
                        estado = 0
                        i-=1

                elif estado == 4:
                    if char == '=':
                        token = Token(char, "LE", "<=", num_linha)
                        tokens.append(token)
                        estado = 0
                    else: 
                        token = Token(char, "LT", "<", num_linha)
                        tokens.append(token)
                        estado = 0
                        i-=1
                
                elif estado == 5:
                    if char == '>':
                        token = Token(char, "ARROW", "->", num_linha)
                        tokens.append(token)
                        estado = 0
                    else:
                        token = Token(char, "MINUS", "-", num_linha)
                        tokens.append(token)
                        estado = 0
                        i-=1

                elif estado == 6:
                    if char == '.':
                        lexema.append(char)
                        estado = 7
                    elif char in string.digits:
                        lexema.append(char)
                    else: 
                        number = ''.join(lexema)
                        token = Token(char, "IntConst", number, num_linha)
                        tokens.append(token)
                        lexema = []
                        estado = 0
                        i-=1

                elif estado == 7:
                    if char in string.digits:
                        lexema.append(char)
                        estado = 8
                
                elif estado == 8:
                    if char in string.digits:
                        lexema.append(char)
                        estado = 8
                    elif char == '.':
                        print("ERRO!")
                    else: 
                        number = ''.join(lexema)
                        token = Token(char, "FloatConst", number, num_linha)
                        tokens.append(token)
                        lexema = []
                        estado = 0
                        i-=1

                elif estado == 9:
                    if char in string.ascii_letters or char in string.digits or char == "_":
                        lexema.append(char) 
                    else: 
                        word = ''.join(lexema)

                        if word in reservadas:
                            token = Token(char, word.upper(), word, num_linha)
                            tokens.append(token)
                        else:
                            token = Token(char, "ID", word, num_linha)
                            tokens.append(token)

                        lexema = []
                        estado = 0  
                        i-=1
                
                elif estado == 10:
                    lexema.append(char)
                    estado = 11
                    
                elif estado == 11:
                    if char == "'":
                        c = ''.join(lexema)
                        token = Token(char, "CharLiteral", c, num_linha)
                        tokens.append(token)
                        lexema = []
                        estado = 0
                
                elif estado == 12:
                    if char in string.ascii_letters or  char == '{':
                        lexema.append(char)
                        estado = 13
                
                elif estado == 13:
                    if char in string.ascii_letters or  char == '}':
                        lexema.append(char)
                    elif char == '"':
                        s = ''.join(lexema)
                        token = Token(char, "FormattedString", s, num_linha)
                        tokens.append(token)
                        lexema = []
                        estado = 0
                    else: 
                        print(f"ERRO linha {num_linha}!")
                        estado = 0

                i+=1
            num_linha += 1

    # Construir a estrutura de dados que será escrita no arquivo JSON
    os.makedirs('json', exist_ok=True)

    token_data = []

    for token in tokens:
        token_data.append({
            "line_number": token.line_number,
            "token_type": token.type,
            "token_name": token.name
        })

    filenameFormatted = file_path.rsplit('.', 1)[0]
    json_filename = os.path.join('json', f'{filenameFormatted}_tokens.json')

    # Escrever a estrutura no arquivo JSON dentro da pasta 'json'
    with open(json_filename, 'w') as json_file:
        json.dump(token_data, json_file, indent=4)

    token = Token("EOF", "EOF", "EOF", "")
    tokens.append(token)
    
    return tokens