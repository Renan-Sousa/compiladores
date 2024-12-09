import sys
from analises.lexico import analizadorLexico
from analises.sintatico import analizadorSintatico

if __name__ == "__main__":
    filename = sys.argv[1]
    vetorTokens = analizadorLexico(filename) 
    analizadorSintatico(vetorTokens)