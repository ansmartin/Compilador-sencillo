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
        self.alex = None  # analizador lexico
        self.c = None     # componente actual


    # coge el siguiente componente en la lista
    def siguiente(self):
        self.c=self.alex.Analiza()
    
    # comprueba que la categoria del componente sea igual
    def compruebacat(self, cat):
        if self.c.cat == cat:
            self.siguiente()
            return True
        else:
            self.error(cat)

    # comprueba que la categoria y el valor del componente sean iguales     
    def compruebacatyvalor(self, cat, valor):
        if self.c.cat == cat:
            if self.c.valor == valor:
                self.siguiente()
                return True
            else:
                self.error(valor)
        else:
            self.error(cat)

    # imprime cual es el error
    def error(self, e):
        print 'Error con ',self.c,'\t Deberia ser: ',e
 

    ############################################################################
    #
    #  Funcion: Analiza
    #  Tarea:  
    #  Parametros:  analex:  analizador lexico
    #  Devuelve: Devuelve 
    #
    ############################################################################
    def Analiza(self, analex):
        self.alex=analex
        self.siguiente()

        if self.analizaPrograma():
            print '\nAnalizado con exito'
        
    
    def analizaPrograma(self):
        if self.compruebacatyvalor('PR','PROGRAMA'):
            if not self.compruebacat('Identif'): return
            if not self.compruebacat('PtoComa'): return
            if not self.analizadecl_var(): return
            if not self.analizainstrucciones(): return
            if not self.compruebacat('Punto'): return
            return True
        else:
            return


    def analizadecl_var(self):
        if self.compruebacatyvalor('PR','VAR'):

            return True
        elif self.compruebacat('INICIO'):

            return True
        else:
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
    analex = analex.Analex(fl)
    
    Anasintac().Analiza(analex)

    i=i+1

    
    
