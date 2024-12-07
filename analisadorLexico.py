import sys
import string
import json

estado = 0  #Estado inicial do AFD

lexema = [] #Variavel que guarda o lexema atualmente reconhecido
tokens = [] #Vetor de tokens

num_linha = 1

class Token:
    def __init__(self, char, type, name, line_number):
        self.char = char
        self.type = type
        self.name = name
        self.line_number = line_number

# AFD
filename = sys.argv[1]
file = open(filename, "r") 

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
                token = Token(char, "Punctuation", "LBRACKET", num_linha)
                tokens.append(token)
            elif char == ')':
                token = Token(char, "Punctuation", "RBRACKET", num_linha)
                tokens.append(token)
            elif char == '{':
                token = Token(char, "Punctuation", "LBRACE", num_linha)
                tokens.append(token)
            elif char == '}':
                token = Token(char, "Punctuation", "RBRACE", num_linha)
                tokens.append(token)
            elif char == ':':
                token = Token(char, "Punctuation", "COLON", num_linha)
                tokens.append(token)
            elif char == ',':
                token = Token(char, "Punctuation", "COMMA", num_linha)
                tokens.append(token)
            elif char == ';':
                token = Token(char, "Punctuation", "SEMICOLON", num_linha)
                tokens.append(token)
            elif char == '+':
                token = Token(char, "Operators", "PLUS", num_linha)
                tokens.append(token)
            elif char == '*':
                token = Token(char, "Operators", "MULT", num_linha)
                tokens.append(token)
            elif char == '/':
                token = Token(char, "Operators", "DIV", num_linha)
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
                token = Token(char, "Operators", "EQ", num_linha)
                tokens.append(token)
                estado = 0
            else:
                token = Token(char, "Operators", "ASSIGN", num_linha)
                tokens.append(token)
                estado = 0
                i-=1

        elif estado == 2:
            if char == '=':
                token = Token(char, "Operators", "NE", num_linha)
                tokens.append(token)
                estado = 0
        
        elif estado == 3:
            if char == '=':
                token = Token(char, "Operators", "GE", num_linha)
                tokens.append(token)
                estado = 0
            else:
                token = Token(char, "Operators", "GT", num_linha)
                tokens.append(token)
                estado = 0
                i-=1

        elif estado == 4:
            if char == '=':
                token = Token(char, "Operators", "LE", num_linha)
                tokens.append(token)
                estado = 0
            else: 
                token = Token(char, "Operators", "LT", num_linha)
                tokens.append(token)
                estado = 0
                i-=1
        
        elif estado == 5:
            if char == '>':
                token = Token(char, "Operators", "ARROW", num_linha)
                tokens.append(token)
                estado = 0
            else:
                token = Token(char, "Operators", "MINUS", num_linha)
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

                if word == "fn":
                    token = Token(char, "ReservedWords", "FUNCTION", num_linha)
                    tokens.append(token)
                elif word == "main":
                    token = Token(char, "ReservedWords", "MAIN", num_linha)
                    tokens.append(token)
                elif word == "let":
                    token = Token(char, "ReservedWords", "LET", num_linha)
                    tokens.append(token)
                elif word == "int":
                    token = Token(char, "ReservedWords", "INT", num_linha)
                    tokens.append(token)
                elif word == "float":
                    token = Token(char, "ReservedWords", "FLOAT", num_linha)
                    tokens.append(token)
                elif word == "char":
                    token = Token(char, "ReservedWords", "CHAR", num_linha)
                    tokens.append(token)
                elif word == "if":
                    token = Token(char, "ReservedWords", "IF", num_linha)
                    tokens.append(token)
                elif word == "else":
                    token = Token(char, "ReservedWords", "ELSE", num_linha)
                    tokens.append(token)
                elif word == "while":
                    token = Token(char, "ReservedWords", "WHILE", num_linha)
                    tokens.append(token)
                elif word == "println":
                    token = Token(char, "ReservedWords", "PRINTLN", num_linha)
                    tokens.append(token)
                elif word == "return":
                    token = Token(char, "ReservedWords", "RETURN", num_linha)
                    tokens.append(token)
                else:
                    token = Token(char, "Identifier", word, num_linha)
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
token_data = []

for token in tokens:
    token_data.append({
        "line_number": token.line_number,
        "token_type": {
            token.type: token.name
        }
    })

filenameFormatted = filename.rsplit('.', 1)[0]
print(filenameFormatted)

# media.p.json

# Escrever a estrutura no arquivo JSON
with open(f'{filenameFormatted}_tokens.json', 'w') as json_file:
    json.dump(token_data, json_file, indent=4)

file.close()