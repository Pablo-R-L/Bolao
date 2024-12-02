import customtkinter
from tkinter import *

class Jogador:
    #nome = "" 
    


    def __init__(self, Fases, Rodadas, Fileira, db, nomedb, osTabs):
        #nomeDiff serve pra saber quando o nome for alterado
        self.nomeDiff = ""
        self.coluna = 0
        self.infos = {
            "Media": None,
            "Fase1":{
                "Rodada1": "0"
            }
        }
        
        self.labelMedia = []
        self.labelMediaRodada = []
        self.textoRodadas = []
        self.nome = []
        self.playerNUmeracao = []
        self.fileira = Fileira
        

        if db != None:
            self.infos = db.copy()
        else:
            for i in range(1, Fases):
                self.infos["Fase" + str(i+1)] = {}
                for rodada in range(Rodadas[i]):
                    self.infos["Fase" + str(i+1)]["Rodada" + str(i)] = "0"

        

        
        for fase in range(Fases):
            self.coluna= self.coluna +10

            self.playerNumeracao = customtkinter.CTkLabel(osTabs[fase], text=" "+str(int(Fileira/10)) + " ", fg_color='#171717')
            self.playerNumeracao.grid(row=Fileira)

            
            birl = customtkinter.CTkTextbox(osTabs[fase], height=1, width=100)
            birl.grid(pady=3, padx=3, column=self.coluna, row=Fileira)
            birl.insert(1.0, nomedb)
            self.nomeDiff = birl.get(0.0, 'end').replace("\n", "")
            self.nome.append(birl)

            for rodada in range(Rodadas[fase]):
                self.coluna = self.coluna + 10
                text = customtkinter.CTkTextbox(osTabs[fase], height=1, width=80)
                self.textoRodadas.append(text)
                text.grid(pady=3, padx=3, column=self.coluna, row=Fileira)
                if db != None:
                    rodadaAtual = "Rodada" + str(rodada+1)
                    faseAtual = "Fase" + str(fase+1)
                    text.insert(1.0, db[faseAtual][rodadaAtual])
                    
            
           
                    
                    
        self.coluna = self.coluna + 1

    #=================================================================================================  
    
    def AddNoJson(self, db, fases, rodadas, mainframe):
        infos = self.infos
        nome = self.nome
        textoDoTextoRodadas  = []
        quantiaRodadas = rodadas#int(len(self.textoRodadas)/fases)
       
        Nome = nome[mainframe].get(0.0, 'end').replace("\n", "")
    
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
    #atualiza as medias
    def getMedia(self, mainframe, rodadaCheck, rodadaPoint):
        media = 0
        #para cada valor de cada rodada
        for mopas in self.textoRodadas:
            #se o valor dentro do bloco é realmente um numero
            if mopas.get(0.0, 'end').replace("\n", "").isnumeric():
                media = media + int(mopas.get(0.0, 'end').replace("\n", ""))
        
        self.infos["Media"] = media
        novoNome = self.nome[mainframe].get(0.0, 'end')
        if novoNome != self.nome[0].get(0.0, 'end') or novoNome != self.nome[len(self.nome)-1].get(0.0, 'end'):
            for nome in range(len(self.nome)):
                if nome != mainframe:
                    self.nome[nome].delete(0.0, 'end')
                    self.nome[nome].insert(0.0, self.nome[mainframe].get(0.0, 'end').replace("\n", ""))

        self.updateAllMedia(mainframe, rodadaCheck, rodadaPoint)
    
    #atualiza a media apenas da aba aberta
    def updateAllMedia(self, mainframe, rodadaCheck, rodadaPoint):
        
       
        self.labelMedia[mainframe].configure(text=self.infos["Media"])
        
        media = 0
        for rodada in range(rodadaCheck, rodadaPoint):
            if self.textoRodadas[rodada].get(0.0, 'end').replace("\n", "").isnumeric():
                media = media + int(self.textoRodadas[rodada].get(0.0, 'end').replace("\n", ""))
    
        self.labelMediaRodada[mainframe].configure(text=media) 


    #cria o label de media de todas as abas
    def setMedia(self, mainframe):
        fi = self.fileira
        lm = self.labelMedia
        if self.labelMediaRodada == []:
            for frame in mainframe:
                
                bedas = customtkinter.CTkLabel(frame, text="0")
                bedas.grid(row=fi, column=self.coluna, pady=3, padx=3)
                self.labelMediaRodada.append(bedas)
                
        
        self.coluna = self.coluna + 10        
        
        if self.labelMedia == []:
            for frame in mainframe:
                
                bedas = customtkinter.CTkLabel(frame, text=self.infos["Media"], fg_color='#171717')
                bedas.grid(row=fi, column=self.coluna, pady=3, padx=3)
                
                lm.append(bedas)
        
        

        

        # for label in self.labelMedia:
        #     label.configure(text=self.infos["Media"])
    
    #=================================================================================================
    
    def sobeDesce(self, pos):
        tr = self.textoRodadas
        nm = self.nome
        lm = self.labelMedia
        lmr = self.labelMediaRodada
        fi = pos #posição desejada

        for i in tr:
            i.grid(row=fi*10)
        
        for nome in nm:
            nome.grid(row=fi*10)
        
        
        for label in lm:
            label.grid(row=fi*10)
        for labelRodada in lmr:
            labelRodada.grid(row=fi*10)
        
        self.fileira = pos*10
        
    #=================================================================================================
    
    




