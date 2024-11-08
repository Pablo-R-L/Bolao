import customtkinter
from tkinter import *
import Commands

fasesNovoBolao = '' #quantia de fases
frameDoNovobola = ''#frame dos combo boxes
fasesLista = [] #labels para inumerar as fases
rodadasLista = [] #combo boxes das rodadas
rodadas = [] #valor dos combo boxes de rodadas^
newBolaoWindow = '' #a janela
fileira = 3 #fileira pro grid
textoNome = '' #Nome do arquivo do novo bolao

#vai criar a nova janela e vai dar start no loop logo abaixo
def criarNovoBolao():
    global fasesNovoBolao, newBolaoWindow, frameDoNovobola, textoNome
    
    #so a nova janela msm
    newBolaoWindow = customtkinter.CTkToplevel()
    newBolaoWindow.title("Especificações Novo Bolão")
    newBolaoWindow.geometry("400x300")

    frameDoNovobola = customtkinter.CTkScrollableFrame(newBolaoWindow, width=500)
    frameDoNovobola.grid(row=10)

    #os labels pra indicar as fases e as rodadas
    customtkinter.CTkLabel(newBolaoWindow, text=" ", height=45).grid(row=0, column=0)
    customtkinter.CTkLabel(newBolaoWindow, text="Fases:").place(x=70, y= 5)
    customtkinter.CTkLabel(newBolaoWindow, text="Rodadas:").place(x=240, y=5)
    fasesNovoBolao = customtkinter.CTkComboBox(frameDoNovobola, values=["1","2","3","4","5","6","7","8","9","10"],width=120)
    fasesNovoBolao.grid(column=0, row=1, padx=40)

    #botao pra finalizar e terminar
    readyB = customtkinter.CTkButton(newBolaoWindow, text="Pronto", command=Allset)
    readyB.grid(row=100)

    textoNome = customtkinter.CTkEntry(newBolaoWindow, placeholder_text="Nome do arquivo", )
    textoNome.place(x=10, y=260)

    
    newBolaoWindow.after(1000,newBolaoWindow.focus())
    
    newBolaoWindow.after(1000, novoBolaoLoop)
    
#======================================================================================================================================================

def Allset():
    global newBolaoWindow
    for i  in rodadasLista:
        rodadas.append(int(i.get()))
    
    if textoNome.get() == ' ' or textoNome.get() == '':
        textoNome.configure(fg_color='red')
        newBolaoWindow.after(400, lambda:textoNome.configure(fg_color='grey'))
    else:
        Commands.criarNovo(fases=int(fasesNovoBolao.get()), rodadas=rodadas, nome=textoNome.get())
        newBolaoWindow.destroy()

#======================================================================================================================================================

once = True
def novoBolaoLoop():
    global fileira, quantasFases, fasesLista, once
    if once == True:
        newBolaoWindow.focus()
        once = False
    
    if fasesNovoBolao.get().isnumeric() and int(fasesNovoBolao.get()) > 0:
        quantasFases = int(fasesNovoBolao.get())
    #print(fasesLista)
    

    if quantasFases > len(fasesLista):
        for i in range(len(fasesLista) + 1, int(quantasFases) + 1):
            rodadasLista.append(customtkinter.CTkComboBox(frameDoNovobola, values=["1","2","3","4","5","6","7","8","9","10"], button_color="#6592db", border_color="#6592db", dropdown_fg_color="#6592db", width=80))
            rodadasLista[i-1].grid(row=fileira, column=3, pady=3)
            fasesLista.append(customtkinter.CTkLabel(frameDoNovobola, text="Fase " + str(i)))
            fasesLista[i-1].grid(row=fileira, pady=3)
            fileira = fileira + 3
            
    elif int(quantasFases) < len(fasesLista):
        salvaFaseListaLen = len(fasesLista)
        for i in range(1, len(fasesLista) - int(quantasFases)+1):
            rodadasLista[salvaFaseListaLen - i].grid_remove()
            del rodadasLista[salvaFaseListaLen - i]
            fasesLista[salvaFaseListaLen - i].grid_remove()
            del fasesLista[salvaFaseListaLen - i]
            fileira = fileira - 3

    newBolaoWindow.after(500, novoBolaoLoop)

    #私のパンツはたわごとでいっぱいです