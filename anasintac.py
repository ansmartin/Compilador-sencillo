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
    #############################################################################
    ##  Conjunto de palabras reservadas para comprobar si un identificador es PR
    #############################################################################
    PR = ImmutableSet(["PROGRAMA", "VAR", "VECTOR","DE", "ENTERO", "REAL", "BOOLEANO", "PROC", "FUNCION", "INICIO", "FIN", "SI", "ENTONCES", "SINO", "MIENTRAS", "HACER", "LEE", "ESCRIBE", "Y", "O", "NO", "CIERTO","FALSO"])
 
 
    #############################################################################
    ##  Rangos para comprobar si un caracter es un numero o una letra valida
    #############################################################################
    numero = range(ord('0'),ord('9')+1)
    letra_minus = range(ord('a'),ord('z')+1)
    letra_mayus = range(ord('A'),ord('Z')+1)
    

    ############################################################################
    #
    #  Funcion: __init__
    #  Tarea:  Constructor de la clase
    #  Parametros:  flujo:  flujo de caracteres de entrada
    #  Devuelve: --
    #
    ############################################################################
    def __init__(self, a, alex):
        self.a=a
        self.alex=alex
        
    ############################################################################
    #
    #  Funcion: Analiza
    #  Tarea:  Identifica los diferentes componentes lexicos
    #  Prametros:  --
    #  Devuelve: Devuelve un componente lexico
    #
    ############################################################################
    def Analiza(self):
        pass

    def analizaPrograma():
        if self.a == "PROGRAMA":
            V

    def analizadecl_var():
        if self.a == "VAR":
            V

    def analizadecl_v():
        if self.a == "PROGRAMA":
            V

    def analizalista_id():

    def analizaresto_listaid():

    def analizatipo():

    def analizatipo_std():

    def analizainstrucciones():

    def analizalista_inst():

    def analizainstruccion():

    def analizainst_simple():

    def analizaresto_instsimple():

    def analizavariable():

    def analizaresto_var():

    def analizainst_es():

    def analizaexpresion():

    def analizaexpresion2():

    def analizaexpr_simple():

    def analizaresto_exsimple():

    def analizatermino():

    def analizaresto_term():

    def analizafactor():

    def analizasigno():

    def analizaPunto():

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
    print "Este es tu fichero %r" % filename
    i=0
    fl = flujo.Flujo(txt)
    analex = Analex(fl)
    
    c=analex.Analiza()
    while c :
        print(c)
        c=analex.Analiza()
    i=i+1
    

    """
    except errores.Error as err :
        sys.stderr.write("%s\n" % err)
        analex.muestraError(sys.stderr)
    """
