import customtkinter
from tkinter import *


#Fachada na parte de cima que aponta as fases rodadas e jogadores
class Lambida:
    def __init__(self, Fases, Rodadas, Fileira, osMainframes, db):
            self.coluna = 0

            self.fileira = Fileira
            self.textoRodadas = []

            #pra cada fase vai rodar um loop de rodadas 
            #e antes de cada loop de rodadas vai registrar uma nova fase
            for fase in range(Fases):
                self.coluna = self.coluna + 10
                #n sei oq é isso aqui
                #mopagano = customtkinter.CTkLabel(osMainframes[fase], height=1, width=10, text="" , text_color="#6c8aba")
                #mopagano.grid(column=self.coluna, row=0, padx=3, pady=10,sticky="n")
                
                self.nome = customtkinter.CTkLabel(osMainframes[fase], height=1, width=100, text="Nome")
                self.nome.grid(pady=10, padx=10, column=self.coluna, row=0, sticky="n")
                
                for rodada in range(Rodadas[fase]):
                    self.coluna = self.coluna + 10
                    text = customtkinter.CTkLabel(osMainframes[fase], height=1, width=80, text= "Rodada " + str(rodada+1))
                    self.textoRodadas.append(text)
                    text.grid(pady=10, padx=3, column=self.coluna, row=0,sticky="n")
                
                self.coluna = self.coluna + 10
                self.somaFase = customtkinter.CTkLabel(osMainframes[fase], height=1, text="Soma Fase")
                self.somaFase.grid(padx=10, column=self.coluna, row=0, sticky="n")
                self.coluna = self.coluna + 10
                self.somaTotal = customtkinter.CTkLabel(osMainframes[fase], height=1, text="Total")
                self.somaTotal.grid(pady=10, padx=10, column=self.coluna, row=0, sticky="n")


                
            
                        
                        
            
    