import customtkinter
from tkinter import *

def tabsArrage(osTabs, db):
    for jog in db:
        if jog != "First":
            pass
            
        else:
            for tab in range(len(osTabs)):
                pass
                
            #como first é sempre o primeiro no json isso aqui roda sempre primeiro
            #serve pra fazer os labes na parte de cima que indicam as fases e as rodadas
            osLabels = Lambida(Fileira=fileira, mainFrame= mainFrame, Fases=quantasFases, Rodadas=quantasRodadas, db=db[jog])
        fileira = fileira + 10