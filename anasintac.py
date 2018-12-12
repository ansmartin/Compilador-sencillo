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
    ##  Lista de identificadores declarados
    #############################################################################
    ids={}

    actual=None


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
    #  Devuelve:
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
                and self.compruebacat('Punto')
                ): return True
        else:
            self.error('PR (valor = PROGRAMA)')


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
            # Comprobacion semantica 1: Dos objetos no pueden tener el mismo nombre
            if self.c.valor in self.ids:
                return self.error('Identif con otro valor distinto, el actual ya esta definido')

            # guardo el identificador en el diccionario de ids
            self.ids[self.c.valor]=self.c
            self.actual=self.c.valor

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
            #
            self.ids[self.actual].tipo=self.c.valor
            
            self.siguiente()
            if self.compruebacat('CorAp'):
                #Comprobacion semantica adicional: No puede haber vectores con un numero real de elementos
                if self.c.cat == 'Numero' and self.c.tipo == 'int':

                    # guardo el tamano del vector para comprobar luego que al acceder se esta dentro del rango
                    self.ids[self.actual].tamvector=self.c.valor

                    self.siguiente()
                    if (
                        self.compruebacat('CorCi')
                        and self.compruebacatyvalor('PR','DE')
                        and self.analizatipo_std()
                    ): return True
                else:
                    self.error('Numero entero')
        else:
            self.error('PR (valor = ENTERO) | PR (valor = REAL) | PR (valor = BOOLEANO) | PR (valor = VECTOR)')


    def analizatipo_std(self):
        if self.c.cat == 'PR' and (self.c.valor in ['ENTERO','REAL','BOOLEANO']):
            # guardo el tipo del identificador
            self.ids[self.actual].tipo=self.c.valor
            
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
        if self.c.cat == 'Identif':
            self.actual = self.c.valor

            #Comprobacion semantica adicional: El identificador debe estar declarado antes de hacerle algo
            if self.c.valor not in self.ids:
                return self.error('Un Identif previamente declarado')
            
            self.siguiente()
            return self.analizaresto_instsimple()

        else:
            self.error('Identif')


    def analizaresto_instsimple(self):
        if self.c.cat == 'OpAsigna':
            self.siguiente()
            return self.analizaexpresion()

        elif self.c.cat == 'CorAp':
            self.siguiente()
            if (
                self.analizaexpr_simple()
                and self.compruebacat('CorCi')
                and self.compruebacat('OpAsigna')
                and self.analizaexpresion()
                ): return True 

        elif (self.c.cat == 'PtoComa') or (self.c.cat == 'PR' and self.c.valor == 'SINO'):
            return True

        else:
            self.error('OpAsigna | CorAp | PtoComa | PR (valor = SINO)')


    def analizavariable(self):
        if self.c.cat == 'Identif':
            
            #Comprobacion semantica adicional: El identificador debe estar declarado antes de hacerle algo
            if self.c.valor not in self.ids:
                return self.error('Un Identif previamente declarado')

            self.siguiente()
            return self.analizaresto_var()

        else:
            self.error('Identif')


    def analizaresto_var(self):
        if self.c.cat == 'CorAp':
            self.siguiente()
            if (
                self.analizaexpr_simple()
                and self.compruebacat('CorCi')
                ): return True 

        elif (self.c.cat in ['OpMult','OpAdd','OpRel','CorCi','ParentCi','PtoComa']) or (self.c.cat == 'PR' and self.c.valor in ['Y','O','ENTONCES','HACER','SINO']):
            return True

        else:
            self.error('CorAp | OpMult | OpAdd | OpRel | CorCi | ParentCi | PtoComa | PR (valor = Y) | PR (valor = O) | PR (valor = ENTONCES) | PR (valor = HACER) | PR (valor = SINO)')



    def analizainst_es(self):
        if self.c.cat == 'PR' and self.c.valor == 'LEE':
            self.siguiente()
            if self.compruebacat('CorAp'):
                if self.c.cat == 'Identif':
                    #Comprobacion semantica 7: En la instruccion LEE el argumento debe ser ENTERO o REAL
                    if self.c.cat.tipo=='ENTERO' or self.c.cat.tipo=='REAL':
                        self.siguiente()   
                        return self.compruebacat('CorCi')

                    
        elif self.c.cat == 'PR' and self.c.valor == 'ESCRIBE':
            self.siguiente()
            if (
                self.compruebacat('ParentAp')
                and self.analizaexpr_simple()
                and self.compruebacat('ParentCi')
                ): return True
        else:
            self.error('PR (valor = LEE) | PR (valor = ESCRIBE)')


    def analizaexpresion(self):
        if (self.c.cat in ['Identif','Numero','ParentAp','OpAdd']) or (self.c.cat == 'PR' and self.c.valor in ['NO','CIERTO','FALSO']):
            if (
                self.analizaexpr_simple()
                and self.analizaexpresion2()
                ): return True
        else:
            self.error('Identif | Numero | ParentAp | OpAdd | PR (valor = NO) | PR (valor = CIERTO | PR (valor = FALSO)')


    def analizaexpresion2(self):
        if self.c.cat == 'OpRel':
            self.siguiente()
            return self.analizaexpr_simple()

        elif (self.c.cat in ['ParentCi','PtoComa']) or (self.c.cat == 'PR' and self.c.valor in ['ENTONCES','HACER','SINO']):
            return True

        else:
            self.error('ParentCi | PtoComa | PR (valor = ENTONCES) | PR (valor = HACER) | PR (valor = SINO)')



    def analizaexpr_simple(self):
        if (self.c.cat in ['Identif','Numero','ParentAp']) or (self.c.cat == 'PR' and self.c.valor in ['NO','CIERTO','FALSO']):
            if (
                self.analizatermino()
                and self.analizaresto_exsimple()
                ): return True

        elif self.c.cat == 'OpAdd':
            if (
                self.analizasigno()
                and self.analizatermino()
                and self.analizaresto_exsimple()
                ): return True

        else:
            self.error('Identif | Numero | ParentAp | OpAdd | PR (valor = NO) | PR (valor = CIERTO | PR (valor = FALSO)')



    def analizaresto_exsimple(self):
        if self.c.cat == 'OpAdd':
            self.siguiente()
            if (
                self.analizatermino()
                and self.analizaresto_exsimple()
                ): return True

        elif self.c.cat == 'PR' and self.c.valor == 'O':
            self.siguiente()
            if (
                self.compruebacatyvalor('PR','O')
                and self.analizatermino()
                and self.analizaresto_exsimple()
                ): return True

        elif (self.c.cat in ['CorCi','OpRel','ParentCi','PtoComa']) or (self.c.cat == 'PR' and self.c.valor in ['ENTONCES','HACER','SINO']):
            return True

        else:
            self.error('OpAdd | CorCi | OpRel | ParentCi | PtoComa | PR (valor = O) | PR (valor = ENTONCES) | PR (valor = HACER) | PR (valor = SINO)')
  


    def analizatermino(self):
        if (self.c.cat in ['Identif','Numero','ParentAp']) or (self.c.cat == 'PR' and self.c.valor in ['NO','CIERTO','FALSO']):
            if (
                self.analizafactor()
                and self.analizaresto_term()
                ): return True
        
        else:
            self.error('Identif | Numero | ParentAp | PR (valor = NO) | PR (valor = CIERTO) | PR (valor = FALSO)')
  

    def analizaresto_term(self):
        if self.c.cat == 'OpMult':
            self.siguiente()
            if (
                self.analizafactor()
                and self.analizaresto_term()
                ): return True

        elif self.c.cat == 'PR' and self.c.valor == 'Y':
            self.siguiente()
            if (
                self.analizafactor()
                and self.analizaresto_term()
                ): return True

        elif (self.c.cat in ['OpAdd','CorCi','OpRel','ParentCi','PtoComa']) or (self.c.cat == 'PR' and self.c.valor in ['O','ENTONCES','HACER','SINO']):
            return True

        else:
            self.error('OpAdd | CorCi | OpRel | ParentCi | PtoComa | PR (valor = O) | PR (valor = ENTONCES) | PR (valor = HACER) | PR (valor = SINO)')
  


    def analizafactor(self):
        if self.c.cat == 'Identif':
            return self.analizavariable()

        elif self.c.cat == 'Numero':
            
            #Comprobacion semantica 5: No hay conversion para los booleanos
            if self.actual in self.ids and self.ids[self.actual].tipo=='BOOLEANO':
                return False

            #Comprobacion semantica 6: El numero debe estar en el rango del vector
            if self.actual in self.ids and self.ids[self.actual].tipo=='VECTOR':
                if self.ids[self.actual].tamvector < self.c.valor:
                    return False

            #Comprobacion semantica 3: Conversion de enteros a reales
            if self.c.tipo == 'int':
                self.c.valor = float(self.c.valor)
                self.c.tipo = 'float'

            self.siguiente()
            return True

        elif self.c.cat == 'ParentAp':
            self.siguiente()
            if (
                self.analizaexpresion()
                and self.compruebacat('ParentCi')
                ): return True

        elif self.c.cat == 'PR' and self.c.valor == 'NO':
            self.siguiente()
            return self.analizafactor()

        elif self.c.cat == 'PR' and self.c.valor == 'CIERTO':
            self.siguiente()
            return True

        elif self.c.cat == 'PR' and self.c.valor == 'FALSO':
            self.siguiente()
            return True
        
        else:
            self.error('Identif | Numero | ParentAp | PR (valor = NO) | PR (valor = CIERTO) | PR (valor = FALSO)')
  


    def analizasigno(self):
        if self.c.cat == 'OpAdd':
            self.siguiente()
            return True
        
        else:
            self.error('OpAdd')

    

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
    
    fl = flujo.Flujo(txt)
    analex = analex.Analex(fl)
    
    Anasintac().Analiza(analex)


    
    
