#!/usr/bin/env python

import componentes
import analex
#import errores
import flujo
import string
import sys

from sys import argv
from sets import ImmutableSet

class Anasintac:

    ############################################################################
    #
    #  Funcion: __init__
    #  Tarea:  Constructor de la clase
    #  Parametros:  --
    #  Devuelve: --
    #
    ############################################################################
    def __init__(self):
        self.c=None     # componente actual
        
    ############################################################################
    #
    #  Funcion: Analiza
    #  Tarea:  
    #  Parametros:  lista_com:  lista de componentes a analizar
    #  Devuelve: Devuelve 
    #
    ############################################################################
    def Analiza(self, lista_com):
        for componente in lista_com:
            self.c = componente

            if self.analizaPrograma():
                return True
            else:
                return False

    def analizaPrograma(self):
        if self.c.cat == 'PR' and self.c.valor == 'PROGRAMA':
            print 'eeeeee'
        else:
            print('Error en linea: '+self.c.linea)
            return


    def analizadecl_var(self):
        if self.c.cat == 'PR':
            if self.c.valor == 'VAR':
                pass
            elif self.c.valor == 'INICIO':
                pass
        else:
            print('Error en linea: '+self.c.linea)
            return

    def analizadecl_v(self):
        pass

    def analizalista_id(self):
        pass

    def analizaresto_listaid(self):
        pass

    def analizatipo(self):
        pass

    def analizatipo_std(self):
        pass

    def analizainstrucciones(self):
        pass

    def analizalista_inst(self):
        pass

    def analizainstruccion(self):
        pass

    def analizainst_simple(self):
        pass

    def analizaresto_instsimple(self):
        pass

    def analizavariable(self):
        pass

    def analizaresto_var(self):
        pass

    def analizainst_es(self):
        pass

    def analizaexpresion(self):
        pass

    def analizaexpresion2(self):
        pass

    def analizaexpr_simple(self):
        pass

    def analizaresto_exsimple(self):
        pass

    def analizatermino(self):
        pass

    def analizaresto_term(self):
        pass

    def analizafactor(self):
        pass

    def analizasigno(self):
        pass

    

############################################################################
#
#  Funcion: __main__
#  Tarea:  Programa principal de prueba del analizador lexico
#  Prametros:  --
#  Devuelve: --
#
############################################################################
if __name__=="__main__":
    script,filename=argv
    txt=open(filename)
    #print "Este es tu fichero %r" % filename
    i=0
    fl = flujo.Flujo(txt)
    alex = analex.Analex(fl)

    com=[]
    c=alex.Analiza()
    while c :
        com.append(c)
        #print(c)
        c=alex.Analiza()
        
    i=i+1

    #print com
    Anasintac().Analiza(com)
    
