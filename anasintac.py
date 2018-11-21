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


    # coge el siguiente componente
    def siguiente(self):
        self.c=self.alex.Analiza()
    """
    # devuelve si la categoria del componente es igual o no
    def igualcat(self, cat):
        return self.c.cat == cat

    # devuelve si la categoria y el valor del componente son iguales o no     
    def igualcatyvalor(self, cat, valor):
        return self.c.cat == cat and self.c.valor == valor
    """
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
                self.error(cat+' (valor = '+valor+')')
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
            print 'Analizado con exito'
        
    
    def analizaPrograma(self):
        if self.c.cat == 'PR' and self.c.valor == 'PROGRAMA':
            self.siguiente()
            if (
                self.compruebacat('Identif')
                and self.compruebacat('PtoComa')
                and self.analizadecl_var()
                and self.analizainstrucciones()
                #and self.compruebacat('Punto')
                ): return True
        else:
            self.error('PR (valor = PROGRAMA)')

        """
        if sself.c.cat == 'PR' and self.c.valor == 'PROGRAMA':
            self.siguiente()
            if self.compruebacat('Identif'):
                self.siguiente()
                if self.compruebacat('PtoComa'):
                    self.siguiente()
                    if self.analizadecl_var():
                        return True
        """    
        


    def analizadecl_var(self):
        if self.c.cat == 'PR' and self.c.valor == 'VAR':
            self.siguiente()
            if (
                self.analizalista_id()
                and self.compruebacat('DosPtos')
                and self.analizatipo()
                and self.compruebacat('PtoComa')
                and self.analizadecl_v()
                ): return True

        elif self.c.cat == 'PR' and self.c.valor == 'INICIO':
            return True

        else:
            self.error('PR (valor = VAR) | PR (valor = INICIO)')


    def analizadecl_v(self):
        if self.c.cat == 'Identif':
            #self.siguiente()
            if (
                self.analizalista_id()
                and self.compruebacat('DosPtos')
                and self.analizatipo()
                and self.compruebacat('PtoComa')
                and self.analizadecl_v()
                ): return True

        elif self.c.cat == 'PR' and self.c.valor == 'INICIO':
            return True

        else:
            self.error('Identif | PR (valor = INICIO)')


    def analizalista_id(self):
        if self.c.cat == 'Identif':
            self.siguiente()
            return self.analizaresto_listaid()
            
        else:
            self.error('Identif')


    def analizaresto_listaid(self):
        if self.c.cat == 'Coma':
            self.siguiente()
            return self.analizalista_id()
                
        elif self.c.cat == 'DosPtos':
            return True

        else:
            self.error('Coma | DosPtos')


    def analizatipo(self):
        if self.c.cat == 'PR' and (self.c.valor in ['ENTERO','REAL','BOOLEANO']):
            return self.analizatipo_std()

        elif self.c.cat == 'PR' and self.c.valor == 'VECTOR':
            self.siguiente()
            if (
                self.compruebacat('CorAp')
                and (self.compruebacat('Numero') and self.c.tipo == int)
                and self.compruebacat('CorCi')
                and self.compruebacatyvalor('PR','DE')
                and self.analizatipo_std()
                ): return True 
        else:
            self.error('PR (valor = ENTERO) | PR (valor = REAL) | PR (valor = BOOLEANO) | PR (valor = VECTOR)')


    def analizatipo_std(self):
        if self.c.cat == 'PR' and (self.c.valor in ['ENTERO','REAL','BOOLEANO']):
            self.siguiente()
            return True
        else:
            self.error('PR (valor = ENTERO) | PR (valor = REAL) | PR (valor = BOOLEANO)')


    def analizainstrucciones(self):
        if self.c.cat == 'PR' and self.c.valor == 'INICIO':
            self.siguiente()
            if (
                self.analizalista_inst()
                and self.compruebacatyvalor('PR','FIN')
                ): return True 
        else:
            self.error('PR (valor = INICIO)')



    def analizalista_inst(self):
        if (self.c.cat == 'PR' and (self.c.valor in ['INICIO','LEE','ESCRIBE','SI','MIENTRAS'])) or self.c.cat == 'Identif':
            if (
                self.analizainstruccion()
                and self.compruebacat('PtoComa')
                and self.analizalista_inst()
                ): return True
        elif self.c.cat == 'PR' and self.c.valor == 'FIN':
            return True
        else:
            self.error('PR (valor = INICIO) | Identif | PR (valor = LEE) | PR (valor = ESCRIBE) | PR (valor = SI) | PR (valor = MIENTRAS) | PR (valor = FIN)')


    def analizainstruccion(self):
        if self.c.cat == 'PR' and self.c.valor == 'INICIO':
            self.siguiente()
            if (
                self.analizalista_inst()
                and self.compruebacatyvalor('PR','FIN')
                ): return True

        elif self.c.cat == 'Identif':
            return self.analizainst_simple()
        elif self.c.cat == 'PR' and (self.c.valor == 'LEE' or self.c.valor == 'ESCRIBE'):   
            return self.analizainst_es()
        elif self.c.cat == 'PR' and self.c.valor == 'SI':
            self.siguiente()
            if (
                self.analizaexpresion()
                and self.compruebacatyvalor('PR','ENTONCES')
                and self.analizainstruccion()
                and self.compruebacatyvalor('PR','SINO')
                and self.analizainstruccion()
                ): return True 

        elif self.c.cat == 'PR' and self.c.valor == 'MIENTRAS':
            self.siguiente()
            if (
                self.analizaexpresion()
                and self.compruebacatyvalor('PR','HACER')
                and self.analizainstruccion()
                ): return True 

        else:
            self.error('PR (valor = INICIO) | Identif | PR (valor = LEE) | PR (valor = ESCRIBE) | PR (valor = SI) | PR (valor = MIENTRAS)')



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

    
    
