#!/usr/bin/env python

import componentes
import analex
#import errores
import flujo
import string
import sys
import AST

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
        self.ids = {}       # tabla de simbolos implementada como un diccionario
        self.ast = []       # arbol de sintaxis abstracta
        self.aux_ast = None   # auxiliar para guardar subarboles
        self.sentencias = []  # lista de sentencias
        self.listavar = []    # lista de variables a declarar
        self.actual = None    # valor del ultimo identificador encontrado
        


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
            print 'Programa analizado con exito'
            print '\n- Tabla de simbolos:\n\n', [str(i) for i in AST.AST().ids.values()]
            print '\n\n- Arbol de sintaxis abstracta:\n\n', self.ast
            
        
 
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
                ): 
                self.listavar=[]

                return self.analizadecl_v()

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
                ): 
                self.listavar=[]

                return self.analizadecl_v()

        elif self.c.cat == 'PR' and self.c.valor == 'INICIO':
            return True

        else:
            self.error('Identif | PR (valor = INICIO)')


    def analizalista_id(self):
        if self.c.cat == 'Identif':

            # guardo el identificador en el diccionario de la tabla de simbolos
            self.ids[self.c.valor]=self.c

            # actualizo la tabla de simbolos en la clase AST
            if AST.AST().actualiza_ids(self.c.valor, self.c):
                
                self.listavar.append(self.c.valor)
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
            self.siguiente()

            if self.compruebacat('CorAp'):
                # Comprobacion semantica adicional: No puede haber vectores con un numero de elementos que no sea entero
                if self.c.cat == 'Numero' and self.c.tipo == 'ENTERO':

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
            # guardo el tipo del identificador o identificadores declarados
            for v in self.listavar:
                self.ids[v].tipo=self.c.valor
            
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
                ):
                # creacion del nodo principal del AST de sentencia compuesta
                self.ast = AST.NodoCompuesta(self.sentencias, self.alex.nlinea)

                return True
        else:
            self.error('PR (valor = INICIO)')



    def analizalista_inst(self):
        if (self.c.cat == 'PR' and (self.c.valor in ['INICIO','LEE','ESCRIBE','SI','MIENTRAS'])) or self.c.cat == 'Identif':
            if (
                self.analizainstruccion()
                and self.compruebacat('PtoComa')
                ): 
                if self.aux_ast != None:
                    self.sentencias.append(self.aux_ast)
                    self.aux_ast=None

                return self.analizalista_inst()
                
        elif self.c.cat == 'PR' and self.c.valor == 'FIN':
            return True
        else:
            self.error('PR (valor = INICIO) | Identif | PR (valor = LEE) | PR (valor = ESCRIBE) | PR (valor = SI) | PR (valor = MIENTRAS) | PR (valor = FIN)')


    def analizainstruccion(self):
        if self.c.cat == 'PR' and self.c.valor == 'INICIO':
            aux_sentencias=self.sentencias
            self.sentencias=[]

            self.siguiente()
            if (
                self.analizalista_inst()
                and self.compruebacatyvalor('PR','FIN')
                ): 
                # creacion de un nodo del AST de sentencia compuesta y lo agrego
                aux_sentencias.append(AST.NodoCompuesta(self.sentencias, self.alex.nlinea))
                self.sentencias=aux_sentencias

                return True

        elif self.c.cat == 'Identif':
            return self.analizainst_simple()

        elif self.c.cat == 'PR' and (self.c.valor == 'LEE' or self.c.valor == 'ESCRIBE'):   
            return self.analizainst_es()

        elif self.c.cat == 'PR' and self.c.valor == 'SI':
            self.siguiente()
            if self.analizaexpresion():
                cond=self.aux_ast
                if (
                    self.compruebacatyvalor('PR','ENTONCES')
                    and self.analizainstruccion()
                    ):
                    si=self.aux_ast
                    if ( 
                        self.compruebacatyvalor('PR','SINO')
                        and self.analizainstruccion()
                        ): 
                        sino=self.aux_ast
                        # creacion de un nodo del AST de si
                        self.aux_ast = AST.NodoSi(cond, si, sino, self.alex.nlinea)
                        return True 

        elif self.c.cat == 'PR' and self.c.valor == 'MIENTRAS':
            self.siguiente()

            if self.analizaexpresion():
                aux=self.aux_ast

                aux_sentencias=self.sentencias
                self.sentencias=[]
                
                if (
                    self.compruebacatyvalor('PR','HACER')
                    and self.analizainstruccion()
                    ): 
                    # creacion de un nodo del AST de mientras
                    aux_sentencias.append(AST.NodoMientras(aux, self.sentencias[0]))
                    self.sentencias=aux_sentencias

                    return True

        else:
            self.error('PR (valor = INICIO) | Identif | PR (valor = LEE) | PR (valor = ESCRIBE) | PR (valor = SI) | PR (valor = MIENTRAS)')



    def analizainst_simple(self):
        if self.c.cat == 'Identif':
            self.actual = self.c.valor

            # creacion de un nodo del AST de acceso a variable
            self.aux_ast = AST.NodoAccesoVariable(self.c.valor, self.alex.nlinea)

            if self.aux_ast.compsemanticas():
                self.siguiente()
                return self.analizaresto_instsimple()

        else:
            self.error('Identif')


    def analizaresto_instsimple(self):
        if self.c.cat == 'OpAsigna':
            self.siguiente()
            
            aux=self.aux_ast

            if self.analizaexpresion():
                # creacion de un nodo del AST de asignacion
                self.aux_ast = AST.NodoAsignacion(aux, self.aux_ast, self.alex.nlinea)

                return self.aux_ast.compsemanticas()

        elif self.c.cat == 'CorAp':
            aux=self.aux_ast
            self.siguiente()
            if (
                self.analizaexpr_simple()
                and self.compruebacat('CorCi')
                ):
                pos=self.aux_ast.valor
                if ( 
                    self.compruebacat('OpAsigna') 
                    and self.analizaexpresion()
                    ): 
                    exp=self.aux_ast
                    # creacion de un nodo del AST de acceso a vector
                    self.aux_ast = AST.NodoAccesoVector(aux, pos, exp, self.alex.nlinea)
                        
                    return self.aux_ast.compsemanticas()

        elif (self.c.cat == 'PtoComa') or (self.c.cat == 'PR' and self.c.valor == 'SINO'):
            return True

        else:
            self.error('OpAsigna | CorAp | PtoComa | PR (valor = SINO)')


    def analizavariable(self):
        if self.c.cat == 'Identif':

            # creacion de un nodo del AST de acceso a variable
            self.aux_ast = AST.NodoAccesoVariable(self.c.valor, self.alex.nlinea)
            
            if self.aux_ast.compsemanticas():
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
            if self.compruebacat('ParentAp'):

                if self.c.cat == 'Identif':
                    # creacion de un nodo del AST de acceso a variable
                    aux = AST.NodoAccesoVariable(self.c.valor, self.alex.nlinea)

                    if aux.compsemanticas():
                        # creacion de un nodo del AST de lee
                        self.aux_ast = AST.NodoLee(aux, self.alex.nlinea)

                        if self.aux_ast.compsemanticas():
                            self.siguiente()
                            return self.compruebacat('ParentCi')

                    
        elif self.c.cat == 'PR' and self.c.valor == 'ESCRIBE':
            self.siguiente()
            if (
                self.compruebacat('ParentAp')
                and self.analizaexpr_simple()
                and self.compruebacat('ParentCi')
                ): 
                # creacion de un nodo del AST de escribe
                self.aux_ast = AST.NodoEscribe(self.aux_ast, self.alex.nlinea)

                return True

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
            op=self.c.valor
            aux=self.aux_ast

            self.siguiente()

            if self.analizaexpr_simple():
                # creacion de un nodo del AST de comparacion
                self.aux_ast = AST.NodoComparacion(op,aux,self.aux_ast,self.alex.nlinea)

                return True

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
            op=self.c.valor
            aux = self.aux_ast

            self.siguiente()
            if (
                self.analizatermino()
                and self.analizaresto_exsimple()
                ): 
                # creacion de un nodo del AST de operacion aritmetica
                self.aux_ast = AST.NodoAritmetica(op,aux,self.aux_ast,self.alex.nlinea)

                return self.aux_ast.compsemanticas()

        elif self.c.cat == 'PR' and self.c.valor == 'O':
            op=self.c.valor
            aux = self.aux_ast

            self.siguiente()
            if (
                self.compruebacatyvalor('PR','O')
                and self.analizatermino()
                and self.analizaresto_exsimple()
                ): 
                # creacion de un nodo del AST de operacion aritmetica
                self.aux_ast = AST.NodoAritmetica(op,aux,self.aux_ast,self.alex.nlinea)
                
                return self.aux_ast.compsemanticas()

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
            op=self.c.valor
            aux = self.aux_ast

            self.siguiente()
            if (
                self.analizafactor()
                and self.analizaresto_term()
                ): 
                # creacion de un nodo del AST de operacion aritmetica
                self.aux_ast = AST.NodoAritmetica(op,aux,self.aux_ast,self.alex.nlinea)

                return self.aux_ast.compsemanticas()

        elif self.c.cat == 'PR' and self.c.valor == 'Y':
            op=self.c.valor
            aux = self.aux_ast
            
            self.siguiente()
            if (
                self.analizafactor()
                and self.analizaresto_term()
                ): 
                # creacion de un nodo del AST de operacion aritmetica
                self.aux_ast = AST.NodoAritmetica(op,aux,self.aux_ast,self.alex.nlinea)

                return self.aux_ast.compsemanticas()

        elif (self.c.cat in ['OpAdd','CorCi','OpRel','ParentCi','PtoComa']) or (self.c.cat == 'PR' and self.c.valor in ['O','ENTONCES','HACER','SINO']):
            return True

        else:
            self.error('OpAdd | CorCi | OpRel | ParentCi | PtoComa | PR (valor = O) | PR (valor = ENTONCES) | PR (valor = HACER) | PR (valor = SINO)')
  


    def analizafactor(self):
        if self.c.cat == 'Identif':
            return self.analizavariable()

        elif self.c.cat == 'Numero':
            
            # creacion de un nodo del AST dependiendo de si el numero es entero o real
            if self.c.tipo == 'ENTERO':
                self.aux_ast = AST.NodoEntero(self.c.valor, self.alex.nlinea)
            elif self.c.tipo == 'REAL':
                self.aux_ast = AST.NodoReal(self.c.valor, self.alex.nlinea)


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
    
    Anasintac().Analiza(analex)
