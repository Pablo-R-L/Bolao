import customtkinter
from tkinter import *

class Jogador:
    nome = "" 
    labelMedia = 0


    def __init__(self, Fases, Rodadas, Fileira, mainFrame, db, nomedb):
        #nomeDiff serve pra saber quando o nome for alterado
        self.nomeDiff = ""
        self.coluna = 0
        self.infos = {
            "Media": None,
            "Fase1":{
                "Rodada1": None
            }
        }
        
        self.fileira = Fileira

        self.fileira = Fileira
        self.textoRodadas = []
        self.nome = customtkinter.CTkTextbox(mainFrame, height=1, width=100)
        self.nome.grid(pady=3, padx=3, column=self.coluna, row=Fileira)
        self.nome.insert(1.0, nomedb)
        self.nomeDiff = self.nome.get(0.0, 'end').replace("\n", "")

        
        for fase in range(Fases):
            self.coluna= self.coluna +10
            #label pra manter um certa distancia entre cada fase
            mopagano = customtkinter.CTkLabel(mainFrame, height=1, width=10, text="")
            mopagano.grid(column=self.coluna, row=Fileira, padx=3, pady=3)
            
            
            for rodada in range(Rodadas[fase]):
                self.coluna = self.coluna + 10
                text = customtkinter.CTkTextbox(mainFrame, height=1, width=80)
                self.textoRodadas.append(text)
                text.grid(pady=3, padx=3, column=self.coluna, row=Fileira)
                if db != None:
                    rodadaAtual = "Rodada" + str(rodada+1)
                    faseAtual = "Fase" + str(fase+1)
                    text.insert(1.0, db[faseAtual][rodadaAtual])
            
           
                    
                    
        self.coluna = self.coluna + 1

    #=================================================================================================  
    
    def AddNoJson(self, db, fases, rodadas):
        infos = self.infos
        nome = self.nome
        textoDoTextoRodadas  = []
        quantiaRodadas = rodadas#int(len(self.textoRodadas)/fases)
       
        Nome = nome.get(0.0, 'end').replace("\n", "")
    
        if Nome != self.nomeDiff and self.nomeDiff in db:        
            del db[self.nomeDiff]
        self.nomeDiff = Nome
        
        #transforma os endereços dos TextBox em textos
        for rodada in range(len(self.textoRodadas)):
            textoDoTextoRodadas.append(self.textoRodadas[rodada].get(0.0, 'end').replace("\n", ""))
            
        pos = 0 #mantem a posição do array de rodadas
        for posi in range(1, fases+1):
            infos["Fase" + str(posi)] = {}
           
            for rodada in range(quantiaRodadas[posi-1]):
                infos["Fase" + str(posi)]["Rodada" + str(rodada+1)] = textoDoTextoRodadas[pos]
                pos = pos + 1
                
        
        if Nome != "":
            db[Nome] = infos
        return db
    
    #=================================================================================================

    def getMedia(self):
        media = 0
        for mopas in self.textoRodadas:
            if mopas.get(0.0, 'end').replace("\n", "").isnumeric():
                media = media + int(mopas.get(0.0, 'end').replace("\n", ""))
        
        self.infos["Media"] = media

    
    #=================================================================================================

    def setMedia(self, mainframe):
        if self.labelMedia == 0:
            self.labelMedia = customtkinter.CTkLabel(mainframe, text=self.infos["Media"], fg_color='#171717')
            self.labelMedia.grid(row=self.fileira, column=self.coluna, pady=3, padx=3)
        
        self.labelMedia.configure(text=self.infos["Media"])
    
    #=================================================================================================
    
    def sobeDesce(self, pos):
        tr = self.textoRodadas
        nm = self.nome
        lm = self.labelMedia
        fi = pos #posição desejada
        for i in tr:
            i.grid(row=fi)
        nm.grid(row=fi)
        lm.grid(row=fi)
        self.fileira = pos
        
    #=================================================================================================
    
    




