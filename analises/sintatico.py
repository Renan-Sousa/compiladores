class Sintatico:
    def __init__(self, tokens: str):
        self.tokens = tokens
        self.idx = 0

    def match(self, toks):
        tok = ""
        for tok in toks:
            if self.tokens[self.idx].type == tok:
                print(f"Token ({self.tokens[self.idx].type}, '{self.tokens[self.idx].name}') reconhecido na entrada.")
                self.idx += 1
                return True
        print(f"ERRO linha {self.tokens[self.idx].line_number} | Esperava {tok}" )
        return False
    
    def Programa(self):
        # print("Ativação de Programa()")
        self.Funcao()
        self.FuncaoSeq()
        if self.tokens[self.idx].type == "EOF":
            print('Fim da análise sintática.')

    def Funcao(self):
        # print("Ativação de Funcao()")
        self.match(["FN"])
        self.NomeFuncao()
        self.match(["LBRACKET"])
        self.ListaParams()
        self.match(["RBRACKET"])
        self.TipoRetornoFuncao()
        self.Bloco()

    def FuncaoSeq(self):
        # print("Ativação de FuncaoSeq()")
        if self.tokens[self.idx].type == "FN":
            self.Funcao()
            self.FuncaoSeq()

    def NomeFuncao(self):
        # print("Ativação de NomeFuncao()")
        parms = ["ID", "MAIN"]
        self.match(parms)
            
    def ListaParams(self):
        # print("Ativação de ListaParams()")
        if self.tokens[self.idx].type == "ID":
            self.match(["ID"])
            self.match(["COLON"])
            self.Type()
            self.ListaParams2()

    def ListaParams2(self):
        # print("Ativação de ListaParams2()")
        if self.tokens[self.idx].type == "COMMA":
            self.match(["COMMA"])
            self.match(["ID"])
            self.match(["COLON"])
            self.Type()
            self.ListaParams2()

    def TipoRetornoFuncao(self):
        # print("Ativação de TipoRetornoFuncao()")
        if self.tokens[self.idx].type == "ARROW": 
            self.match(["ARROW"])
            self.Type()
        
    def Bloco(self):
        # print("Ativação de Bloco()")
        self.match(['LBRACE'])
        self.Sequencia()
        self.match(['RBRACE'])
        
    def Sequencia(self):
        # print("Ativação de Sequencia()")
        parms = ["ID", "IF", "WHILE", "PRINTLN", "RETURN"]
        if self.tokens[self.idx].type in parms:
            self.Comando()
            self.Sequencia()
        elif self.tokens[self.idx].type == "LET":
            self.Declaracao()
            self.Sequencia()

    def Declaracao(self):
        # print("Ativação de Declaracao()")
        self.match(['LET'])
        self.VarList()
        self.match(['COLON'])
        self.Type()
        self.match(['SEMICOLON'])

    def VarList(self):
        # print("Ativação de VarList()")
        self.match(["ID"])
        self.VarList2()

    def VarList2(self):
        # print("Ativação de VarList2()")
        if self.tokens[self.idx].type == "COMMA":
            self.match(["COMMA"])
            self.match(["ID"])
            self.VarList2()
    
    def Type(self):
        # print("Ativação de Type()")
        parms = ["INT", "FLOAT", "CHAR"]
        self.match(parms)

    def Comando(self):
        # print("Ativação de Comando()")
        if self.tokens[self.idx].type == "ID":
            self.match(["ID"])
            self.AtribuicaoOuChamada()
        elif self.tokens[self.idx].type == "IF":
            self.ComandoSe()
        elif self.tokens[self.idx].type == "WHILE":
            self.match(["WHILE"])
            self.Expr()
            self.Bloco()
        elif self.tokens[self.idx].type == "PRINTLN":
            self.match(["PRINTLN"])
            self.match(["LBRACKET"])
            self.match(["FormattedString"])
            self.match(["COMMA"])
            self.ListaArgs()
            self.match(["RBRACKET"])
            self.match(["SEMICOLON"])
        else:
            self.match(["RETURN"])
            self.Expr()
            self.match(["SEMICOLON"])

    def AtribuicaoOuChamada(self):
        # print("Ativação de AtribuicaoOuChamada()")
        if self.tokens[self.idx].type == "ASSIGN":
            self.match(["ASSIGN"])
            self.Expr()
            self.match(["SEMICOLON"])
        else:
            self.match(["LBRACKET"])
            self.ListaArgs()
            self.match(["RBRACKET"])
            self.match(["SEMICOLON"])

    def ComandoSe(self):
        # print("Ativação de ComandoSe()")
        if self.tokens[self.idx].type == "IF":
            self.match(["IF"])
            self.Expr()
            self.Bloco()
            self.ComandoSenao()
        else: 
            self.Bloco()
        
    def ComandoSenao(self):
        # print("Ativação de ComandoSenao()")
        if self.tokens[self.idx].type == "ELSE":
            self.match(["ELSE"])
            self.ComandoSe()       

    def Expr(self):
        # print("Ativação de Expr()")
        self.Rel()
        self.ExprOpc()

    def ExprOpc(self):
        # print("Ativação de ExprOpc()")
        if self.tokens[self.idx].type == "EQ" or self.tokens[self.idx].type == "NE":
           self.OpIgual()
           self.Rel() 
           self.ExprOpc()

    def OpIgual(self):
        # print("Ativação de OpIgual()")
        parms = ["EQ", "NE"]
        self.match(parms)
        
    def Rel(self):
        # print("Ativação de Rel()")
        self.Adicao()
        self.RelOpc()

    def RelOpc(self):
        # print("Ativação de RelOpc()")
        if self.tokens[self.idx].name == "<" or self.tokens[self.idx].name == "<=" or self.tokens[self.idx].name == ">" or self.tokens[self.idx].name == ">=":
            self.OpRel()
            self.Adicao()
            self.RelOpc()

    def OpRel(self):
        # print("Ativação de OpRel()")
        parms = ["LT", "LE", "GT", "GE"]
        self.match(parms)

    def Adicao(self):
        # print("Ativação de Adicao()")
        self.Termo()
        self.AdicaoOpc()

    def AdicaoOpc(self):
        # print("Ativação de AdicaoOpc()")
        if self.tokens[self.idx].name == "+" or self.tokens[self.idx].name == "-":
            self.OpAdicao()
            self.Termo()
            self.AdicaoOpc()

    def OpAdicao(self):
        # print("Ativação de OpAdicao()")
        parms = ["PLUS", "MINUS"]
        self.match(parms)

    def Termo(self):
        # print("Ativação de Termo()")
        self.Fator()
        self.TermoOpc() 

    def TermoOpc(self):
        # print("Ativação de TempoOc()")
        if self.tokens[self.idx].name == "*" or self.tokens[self.idx].name == "/":
           self.OpMult()
           self.Fator()
           self.TermoOpc()  

    def OpMult(self):
        # print("Ativação de OpMult()")
        parms = ["MULT", "DIV"]
        self.match(parms)
       
    def Fator(self):
        # print("Ativação de Fator()")
        if self.tokens[self.idx].type == "ID":
            self.match(['ID'])
            self.ChamadaFuncao()
        elif self.tokens[self.idx].name == "(":
            self.match(['LBRACKET'])
            self.Expr()
            self.match(['RBRACKET'])
        else:
            parms = ["IntConst", "FloatConst", "CharLiteral"]
            self.match(parms)
            
    def ChamadaFuncao(self):
        # print("Ativação de ChamadaFuncao()")
        if self.tokens[self.idx].name in "(":
            self.match(['LBRACKET'])
            self.ListaArgs()
            self.match(['RBRACKET'])

    def ListaArgs(self):
        # print("Ativação de ListaArgs()")
        parms = ["ID", "IntConst", "FloatConst", "CharLiteral"]
        if self.tokens[self.idx].type in parms: 
            self.Arg()
            self.ListaArgs2()

    def ListaArgs2(self):
        # print("Ativação de ListaArgs2()")
        if self.tokens[self.idx].name in ",": 
            self.match(['COMMA'])
            self.Arg()
            self.ListaArgs2()

    def Arg(self):
        # print("Ativação de Args()")
        if self.tokens[self.idx].type == "ID":
            self.match(['ID'])
            self.ChamadaFuncao()
        else:   
            parms = ["IntConst", "FloatConst", "CharLiteral"]
            self.match(parms)

def analizadorSintatico(vetorTokens): 
    parser = Sintatico(vetorTokens)
    parser.Programa()
 