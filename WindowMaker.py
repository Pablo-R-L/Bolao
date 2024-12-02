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


#caso tiver algum erro, indetifique ele com essa variavel
erro = 0 # 1 = arquivo não encontrado

#abre o arquivo onde ta o local do jason com o save
with open("Saves\\Save.txt", "r") as bedas:
    save = list(bedas)

#abre o arquivo do json e copia pro database (db)
try:
    with open(save[2][:-1], "r") as file:
        db = json.load(file)
except:
    erro = 1
    with open("Saves/Exemplo.json", "r") as file:
        db = json.load(file)
    
    
    with open(save[2][:-1], "w") as gano:
        json.dump(db, gano, indent=4)

fileira = 10 #mantem em conta a proxima fileira livre
jogadores = []
quantasFases = len(db["First"]) -1 #-1 por causa da media
quantasRodadas = []
pause = False #pausa o loop
osLabels = ""
mediaOrdem = True #True para organizar pela media total e false pra media de cada rodada

tabPai = "" #tabview onde os tabs vao ser adcionados
osTabs = [] #lista dos tabs para facil acesso na memoria
osMainFrames =[] #cada tab vai ter que ter um mainframe
playerNumeracao =[]

#==========================================================================================================================================

#Inicia ne porra sabe ler n?
def iniciarK():
    global jogadores, fileira, quantasFases, quantasRodadas, osLabels, tabPai, osTabs, pause
    fileira = 10 #mantem em conta a proxima fileira livre
    jogadores = []
    quantasFases = len(db["First"]) -1 #-1 pra n contar com o atributo "media" que ta no arquivo jason
    quantasRodadas = [] #como cada fase tem uma quantia diferente de rodadas, a quantia de rodadas é salva em uma lista
    
    #conta quantas fases tem na rodada
    for fase in db["First"]:
        #dnv desconsidera o atributo "media"
        if "Media" not in fase:    
            quantasRodadas.append(len(db["First"][fase]))
    
    
    #primeiro pra cada fase tem que ter um tab
    #pra cada tab tem que ter um main frame
    # tabPai = customtkinter.CTkTabview(root, command=tabChange)
    # tabPai.pack(fill = BOTH, expand=1)
    
        
    rod = 0 
    for rodadas in db["First"]:
        if rodadas != "Media":
                rod = rod+1
                newTab = tabPai.add("Fase " + str(rod))
                osTabs.append(newTab)
                geck = CTkXYFrame(newTab)
                geck.pack(fill = BOTH, expand=1)  
                osMainFrames.append(geck)
        
    
    
    for jog in db:
        if jog != "First":
            
            jogadores.append(Jogador(Fileira=fileira, osTabs=osMainFrames, Fases=quantasFases, Rodadas=quantasRodadas, nomedb=jog, db=db[jog]))
            
            fileira = fileira + 10
        else:
            osLabels = Lambida(Fileira=fileira, osMainframes= osMainFrames, Fases=quantasFases, Rodadas=quantasRodadas, db=db[jog])
            fileira = fileira + 20
    
    for jogador in jogadores:
        jogador.setMedia(osMainFrames)
    
    pause = False
        
    
    


#==========================================================================================================================================

#salvar no arquivo json
def salvar():
    global db
    #a aba q está aberta
    tabAtual = tabPai.index(tabPai.get())
    #reorganiza baseado na media
    Commands.mediaOrdemList(jogadores, mediaOrdem, tabAtual)
    
    for i in jogadores:
        db = i.AddNoJson(db, quantasFases, quantasRodadas, tabAtual)

    #atualiza o nome do json que vai abrir junto com o app
    with open(save[2][:-1], "w") as gano:
        json.dump(db, gano, indent=4)

#é chamado quando apertar ctrl+s
def salvarAtalho(event):
    salvar()

#==========================================================================================================================================
def chamaNovoBolao():
    global save, pause
    pause = True
    readyButton = novoBolao.criarNovoBolao()
    readyButton.configure(command = Allset)
    

def Allset():
    global pause, save, db
    
    for i  in  novoBolao.rodadasLista:
        novoBolao.rodadas.append(int(i.get()))
    
    #se o nome do arquivo estiver vazio, otexto vai ficar vermelho
    if  novoBolao.textoNome.get() == ' ' or  novoBolao.textoNome.get() == '':
        novoBolao.textoNome.configure(fg_color='red')
        novoBolao.newBolaoWindow.after(400, lambda: novoBolao.textoNome.configure(fg_color='grey'))
    else:
        
        pause = True
        Commands.criarNovo(fases=int(novoBolao.fasesNovoBolao.get()), rodadas= novoBolao.rodadas, nome= novoBolao.textoNome.get())
        
        #atualiza o save pra iniciar no ultimo bolao q foi aberto
        #deixa root.filename legivel 
        save[2] = "Saves/"+str(novoBolao.textoNome.get()+".json\n")
        #save[2] = save[2][save[2].index("=") + 2 : save[2].index("mode='r'") - 2] + "\n"
        #atualiza o arquivo que indica o ultimo bolao aberto
        with open("Saves\\Save.txt", "w") as file:
            file.writelines(save)

        substituirBolao(save[2][:-1])


        iniciarK()
        
        novoBolao.newBolaoWindow.destroy()

        return



#==========================================================================================================================================

def abrir():
    global db, save, pause
    #abre a janela com os arquivos
    root.filename = filedialog.askopenfile(initialdir="Saves", title="Escolha um Bolao", filetypes=(("json files", "*.json"),("all files", "*.*")))
    
    if root.filename != None or str(root.filename) != "None":
        #atualiza o save pra iniciar no ultimo bolao q foi aberto
        #deixa root.filename legivel 
        save[2] = str(root.filename)
        save[2] = save[2][save[2].index("=") + 2 : save[2].index("mode='r'") - 2] + "\n"
        #atualiza o arquivo que indica o ultimo bolao aberto
        with open("Saves\\Save.txt", "w") as file:
            file.writelines(save)

        substituirBolao(save[2][:-1])


        iniciarK()
        pause=False


#==========================================================================================================================================
def mudarMediaAtalho(event):
    mudarMedia()

def mudarMedia():
    global mediaOrdem
    if mediaOrdem == True:
        mainMenu.menu.entryconfig(3,label="Ordenar por Total")
        mediaOrdem = False
    else:
        mainMenu.menu.entryconfig(3, label="Ordenar por Rodada")
        mediaOrdem = True

#==========================================================================================================================================

def substituirBolao(save):
    global db, pause, osLabels, tabPai, osMainFrames, osTabs
    #Se não pausar o app vai continuar tentando pegar e organizar as medias e vai crashar
    pause = True
    with open(save, "r") as mopa:
        db = json.load(mopa)
    


    #remove todos os wdgets antigos e apaga os objetos
    del osLabels
    #pra cada jogador vai remover tudo e no final apagar o endereço do jogador da memoria
    for jog in jogadores:
        for i in range(len(jog.nome)):
            jog.nome[i].grid_remove()
            jog.labelMedia[i].grid_remove()
        for rodadas in jog.textoRodadas:
            rodadas.grid_remove()
        del jog
    
    
    for i in osMainFrames:
       del i
    for i in range(len(osTabs)):
        tabPai.delete("Fase " + str(i+1))
   
    osTabs.clear()
    osMainFrames.clear()
    

#==========================================================================================================================================

#adciona um jogador com o botao "Add"
def addJogador():
    global jogadores, fileira, pause
    jogadores.append(Jogador(Fileira=fileira, osTabs=osMainFrames, Fases=quantasFases, Rodadas=quantasRodadas, db=None, nomedb=""))
    fileira = fileira + 10
    
    jogadores[len(jogadores)-1].setMedia(osMainFrames)
    

def addJogadorAtalho(event):
    addJogador()

#==============================================================================================================================================

#loop geral da janela
inicial = True
def loop():
    global inicial
    
    #so acontece uma vez
    if inicial:
        inicial = False
        # for jogador in jogadores:
        #     jogador.setMedia(osMainFrames)

    if not pause:
        #a aba q está aberta
        tabAtual = tabPai.index(tabPai.get())
        rodadaCheck = 0#diz onde começa o rodada
        for i in range(tabAtual):
            rodadaCheck = quantasRodadas[i] + rodadaCheck
        rodadaPoint = quantasRodadas[tabAtual] + rodadaCheck#diz ate onde vai a rodada
        

        
        #atualiza a media dos jogadores
        for jogador in jogadores:    
            jogador.getMedia(tabAtual, rodadaCheck, rodadaPoint)
        
      
        #atualiza o jogador mais foda da rodada
        salvestate = 0
        for i in quantasRodadas:
            for rows in range(salvestate, i + salvestate):
            
                salvestate = salvestate + 1
                Commands.firstRodada(rows, jogadores)
        

    root.after(1000, loop)  #a cada segundo

#==========================================================================================================================================
def tabChange():
    if mediaOrdem == False:
        #a aba q está aberta
        tabAtual = tabPai.index(tabPai.get())
        #reorganiza baseado na media
        Commands.mediaOrdemList(jogadores, mediaOrdem, tabAtual)

#==========================================================================================================================================

#so inicia a janela------------------------------------------------------------------------------------------
root = customtkinter.CTk()
root.geometry("750x450")


#cria os botoes da janela
mainMenu = Menubutton(root, text='Menu', relief="raised", bg="#545454", activebackground="#6e6e6e", )
mainMenu.pack(anchor="w")
mainMenu.menu = Menu(mainMenu, tearoff=0)
mainMenu["menu"] = mainMenu.menu
mainMenu.menu.add_command(label="Salvar", command=salvar)
mainMenu.menu.add_command(label="Novo Bolao", command=chamaNovoBolao)
mainMenu.menu.add_command(label="Carregar", command=abrir)
mainMenu.menu.add_command(label="Ordenar por rodada", command=mudarMedia)



tabPai = customtkinter.CTkTabview(root, command=tabChange)
tabPai.pack(fill = BOTH, expand=1)



root.bind("<Control-s>", salvarAtalho)
root.bind("<Control-d>", mudarMediaAtalho)
root.bind("<Control-n>", addJogadorAtalho)

#botao de add jogador
customtkinter.CTkButton(root, cursor="hand2", text='Novo Participante', command=addJogador, width=3, height=35).pack(side=LEFT, anchor=S)
#label pra separar
customtkinter.CTkLabel(root, text='                                       ').pack(side=LEFT, anchor=S)
#sistema de busca
busca = customtkinter.CTkTextbox(root, height=1, width=100, fg_color='#b8b2b2', border_color="#636363", border_width=5, activate_scrollbars=False)
busca.pack(side=LEFT, anchor=S)
customtkinter.CTkButton(root, cursor="hand2", text='Buscar', command=addJogador, width=3, height=35).pack(side=LEFT, anchor=S)
root.after(100,loop) 

if erro != 0:
    messagebox.showinfo(title="Arquivo não encontrado", message="O ultimo arquivo aberto não pôde ser encontrado na pasta \"Saves\".\nCriando um novo arquivo...")

#coloca os usuarios do json na tela
iniciarK()

def printQUaolc():
    print("Qualdwea")

#inicia
root.mainloop()

