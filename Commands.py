#21:40
import json
import customtkinter
from tkinter import *

#pegar o primeiro da rodada
def firstRodada(rodada, jogadores):
    maior = 0
    marcar = ''
    
    for i in jogadores:
        valor = i.textoRodadas[rodada].get(0.0, 'end').replace("\n", "")
        if valor != "" and valor.isnumeric():
            valor = int(valor)
        else:
            valor = 0
    
        if maior < valor:
            maior = valor
            marcar = i #quem vai marcar como O primeiro

    for i in jogadores:    
        if i != marcar:
           i.textoRodadas[rodada].configure(border_width=0, fg_color='#1c1c1c')
           
    #print(marcar.textoRodadas[rodada].get(0.0, 'end'))
    if marcar != '':
        marcar.textoRodadas[rodada].configure(border_width=2, border_color='#ffe08a', fg_color='#363635')
#colocar a lista em sequecia do com maior media pro com menor media

#=============================================================================================================

#meio obvio ne, recebe so o array dos jogadores
def ordemMedia(jogadores):
    arrombados = jogadores.copy()
    bct = True
    while bct:
        trocou = False
        for i in range(len(arrombados)):
            if i+1 < len(arrombados) and arrombados[i].infos["Media"] < arrombados[i+1].infos["Media"]:
                trocou = True
                placeholder = arrombados[i]
                arrombados[i] = arrombados[i+1]
                arrombados[i+1] = placeholder
                
        
        if trocou == False: 
            bct = False


    return(arrombados)

#---------------------------------------------------------------------------------------------------------------

def mediaOrdemList(jogadores):
    osFudidos = ordemMedia(jogadores)
    for fud in range(len(osFudidos)):
        osFudidos[fud].sobeDesce(fud+1)

#=============================================================================================================

def criarNovo(fases, rodadas, nome):
    db = {}
    db["First"] = {}
    db["First"]["Media"] = 0
    for f in range(1, fases+1):
        db["First"]["Fase" + str(f)] = {}
        for r in range(rodadas[f-1]):
            db["First"]["Fase" + str(f)]["Rodada" + str(r+1)] = 0

    with open(f"Bolao\\Saves\\{nome}.json", "w") as gano:
        json.dump(db, gano, indent=4)
    return db

    
    
