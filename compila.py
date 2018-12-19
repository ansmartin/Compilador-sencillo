#!/usr/bin/env python

import componentes
import analex
import anasintac
import flujo
import string
import sys
import AST

from sys import argv
from sets import ImmutableSet

############################################################################
#
#  Funcion: __main__
#  Tarea:  Programa principal
#  Prametros:  --
#  Devuelve: --
#
############################################################################
if __name__=="__main__":
    script,filename=argv
    txt=open(filename)
    #print "Este es tu fichero %r" % filename
    
    fl = flujo.Flujo(txt)
    analex = analex.Analex(fl)
    
    anasintac.Anasintac().Analiza(analex)
