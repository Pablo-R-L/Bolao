#https://customtkinter.tomschimansky.com/documentation/appearancemode/
import customtkinter
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import json

from JogaeJoga import Jogador
from Labels import Lambida
import Commands
import novoBolao
from CTkXYFrame import *

#TODO -- atualizar o local relativo do json exemplo caso o json procurado n exista

#caso tiver algum erro, indetifique ele com essa variavel
erro = 0 # 1 = arquivo não encontrado

#abre o arquivo onde ta o local do jason com o save
with open("Bolao\\Saves\\Save.txt", "r") as bedas:
    save = list(bedas)

#abre o arquivo do json e copia pro database (db)
try:
    with open(save[2][:-1], "r") as file:
        db = json.load(file)
except:
    erro = 1
    with open("Bolao/Saves/Exemplo.json", "r") as file:
        db = json.load(file)
    
    
    with open(save[2][:-1], "w") as gano:
        json.dump(db, gano, indent=4)

fileira = 10 #mantem em conta a proxima fileira livre
jogadores = []
quantasFases = len(db["First"]) -1 #-1 por causa da media
quantasRodadas = []
pause = False #pausa o loop
osLabels = ""
osTabs = []

#==========================================================================================================================================

#Inicia ne porra sabe ler n?
def iniciarK():
    global jogadores, fileira, quantasFases, quantasRodadas, osLabels
    fileira = 10 #mantem em conta a proxima fileira livre
    jogadores = []
    quantasFases = len(db["First"]) -1 #-1 pra n contar com o atributo "media" que ta no arquivo jason
    quantasRodadas = [] #como cada fase tem uma quantia diferente de rodadas, a quantia de rodadas é salva em uma lista
    
    #conta quantas fases tem na rodada
    for fase in db["First"]:
        #dnv desconsidera o atributo "media"
        if "Media" not in fase:    
            quantasRodadas.append(len(db["First"][fase]))
    
    
    #para cada jogador, sem contar o placeholder "First", ele vai ser adcionado no array de objetos "jogadores"
    for jog in db:
        if jog != "First":
            jogadores.append(Jogador(Fileira=fileira, mainFrame=mainFrame, Fases=quantasFases, Rodadas=quantasRodadas, nomedb=jog, db=db[jog]))
        else:
            #como first é sempre o primeiro no json isso aqui roda sempre primeiro
            #serve pra fazer os labes na parte de cima que indicam as fases e as rodadas
            osLabels = Lambida(Fileira=fileira, mainFrame= mainFrame, Fases=quantasFases, Rodadas=quantasRodadas, db=db[jog])
        fileira = fileira + 10

#==========================================================================================================================================

#salvar no arquivo json
def salvar():
    global db
    #reorganiza baseado na media
    Commands.mediaOrdemList(jogadores)
    for i in jogadores:
        db = i.AddNoJson(db, quantasFases, quantasRodadas)

    #atualiza o nome do json que vai abrir junto com o app
    with open(save[2][:-1], "w") as gano:
        json.dump(db, gano, indent=4)

#é chamado quando apertar ctrl+s
def salvarAtalho(event):
    print("foi")
    salvar()

#==========================================================================================================================================
def chamaNovoBolao():
    novoBolao.criarNovoBolao()

#==========================================================================================================================================

def abrir():
    global db, save
    #abre a janela com os arquivos
    root.filename = filedialog.askopenfile(initialdir="Bolao\\Saves", title="Escolha um Bolao", filetypes=(("json files", "*.json"),("all files", "*.*")))
    
    if root.filename != None or root.filename != ' ':
        #atualiza o save pra iniciar no ultimo bolao q foi aberto
        #deixa root.filename legivel 
        save[2] = str(root.filename)
        save[2] = save[2][save[2].index("=") + 2 : save[2].index("mode='r'") - 2] + "\n"
        #atualiza o arquivo que indica o ultimo bolao aberto
        with open("Bolao\\Saves\\Save.txt", "w") as file:
            file.writelines(save)

        substituirBolao(save[2][:-1])


        iniciarK()

#==========================================================================================================================================

def substituirBolao(save):
    global db, pause, osLabels
    #Se não pausar o app vai continuar tentando pegar e organizar as medias e vai crashar
    pause = True
    with open(save, "r") as mopa:
        db = json.load(mopa)
    


    #remove todos os wdgets antigos e apaga os objetos
    del osLabels
    for jog in jogadores:
        jog.nome.grid_remove()
        jog.labelMedia.grid_remove()
        for rodadas in jog.textoRodadas:
            rodadas.grid_remove()
        del jog
    pause = False

#==========================================================================================================================================

#adciona um jogador com o botao "Add"
def addJogador():
    global jogadores, fileira
    jogadores.append(Jogador(Fileira=fileira, mainFrame=mainFrame, Fases=quantasFases, Rodadas=quantasRodadas, db=None, nomedb=""))
    fileira = fileira + 100

#==============================================================================================================================================

#loop geral da janela
inicial = True
def loop():
    global inicial
    
    if not pause:
        #atualiza a media dos jogadores
        for jogador in jogadores:
            jogador.getMedia()
            jogador.setMedia(mainFrame)
      
        #atualiza o jogador mais foda da rodada
        salvestate = 0
        for i in quantasRodadas:
            for rows in range(salvestate, i + salvestate):
            
                salvestate = salvestate + 1
                Commands.firstRodada(rows, jogadores)
        
    #so acontece uma vez
    if inicial:
        inicial = False
        Commands.mediaOrdemList(jogadores)

    root.after(1000, loop)  #a cada segundo

#==========================================================================================================================================

#so inicia a janela------------------------------------------------------------------------------------------
root = customtkinter.CTk()
root.geometry("600x300")


#cria os botoes da janela
mainMenu = Menubutton(root, text='...', relief="raised", bg="#545454", activebackground="#6e6e6e", )
mainMenu.pack(anchor="w")
mainMenu.menu = Menu(mainMenu, tearoff=0)
mainMenu["menu"] = mainMenu.menu
mainMenu.menu.add_command(label="Salvar", command=salvar)
mainMenu.menu.add_command(label="Novo Bolao", command=chamaNovoBolao)
mainMenu.menu.add_command(label="Carregar", command=abrir)





mainFrame = CTkXYFrame(root)
mainFrame.pack(fill = BOTH, expand=1)

root.bind("<Control-s>", salvarAtalho)

customtkinter.CTkButton(root, cursor="hand2", text='Add', command=addJogador, width=3).pack(side=LEFT)
root.after(100,loop) 

if erro != 0:
    messagebox.showinfo(title="Arquivo não encontrado", message="O ultimo arquivo aberto não pôde ser encontrado na pasta \"Saves\".\nCriando um novo arquivo...")

#coloca os usuarios do json na tela
iniciarK()

#inicia
root.mainloop()

