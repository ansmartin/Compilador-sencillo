#!/usr/bin/env python

import componentes
#import errores
import flujo
import string
import sys

from sys import argv
from sets import ImmutableSet

class Analex:
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
    def __init__(self, flujo_caracteres):
        #Debe completarse con  los campos de la clase que se consideren necesarios
        self.nlinea=1 #contador de lineas para identificar errores
        self.fl = flujo_caracteres
        
    ############################################################################
    #
    #  Funcion: Analiza
    #  Tarea:  Identifica los diferentes componentes lexicos
    #  Prametros:  --
    #  Devuelve: Devuelve un componente lexico
    #
    ############################################################################
    def Analiza(self):
        
        ch=self.fl.siguiente()

        if ch==" ":
            # quitar todos los caracteres blancos 
            #buscar el siguiente componente lexico que sera devuelto )
            return self.Analiza()

        elif ch=='':
            # cuando ya no encuentre nada acaba
            return

        elif ch=="+" or ch=="-":
            # debe crearse un objeto de la clasee OpAdd que sera devuelto
            return componentes.OpAdd(ch,self.nlinea)
        
        elif ch=="*" or ch=="/":
            # debe crearse un objeto de la clasee OpMult que sera devuelto
            return componentes.OpMult(ch,self.nlinea)
        
        elif ch=="=":
            # debe crearse un objeto de la clasee OpRel que sera devuelto
            return componentes.OpRel(ch,self.nlinea)
            
        elif ch=="<":
            # debe crearse un objeto de la clasee OpRel que sera devuelto
            ch2=self.fl.siguiente()
            
            if ch2==">":
                return componentes.OpRel(ch+ch2,self.nlinea)
            elif ch2=="=":
                return componentes.OpRel(ch+ch2,self.nlinea)
            else:
                return componentes.OpRel(ch,self.nlinea)
                
        elif ch==">":
            # debe crearse un objeto de la clasee OpRel que sera devuelto
            ch2=self.fl.siguiente()
            
            if ch2=="=":
                return componentes.OpRel(ch+ch2,self.nlinea)
            else:
                return componentes.OpRel(ch,self.nlinea)
            
        #asi con todos los simbolos y operadores del lenguaje
        
        elif ch==",":
            return componentes.Coma()
        
        elif ch=="(":
            return componentes.ParentAp()
        elif ch==")":
            return componentes.ParentCi()
        
        elif ch=="[":
            return componentes.CorAp()
        elif ch=="]":
            return componentes.CorCi()
            
        elif ch==".":
            return componentes.Punto()
            
        elif ch==";":
            return componentes.PtoComa()
        
        elif ch == "{":
            #Saltar todos los caracteres del comentario 
            # y encontrar el siguiente componente lexico
            while ch!="}":
                ch=self.fl.siguiente()

            return self.Analiza()
            
        elif ch == "}":
            print("ERROR: Comentario no abierto") # tenemos un comentario no abierto
            return self.Analiza()
        
        elif ch==":":
            #Comprobar con el siguiente caracter si es una definicion de la declaracion o el operador de asignacion
            ch=self.fl.siguiente()
            
            if ch=="=":
                return componentes.OpAsigna()
            else:
                self.fl.devuelve(ch)
                return componentes.DosPtos()

        # Compruebo si el valor ascii del caracter esta en el rango de las letras posibles
        elif ord(ch) in self.letra_minus or ord(ch) in self.letra_mayus:
            
            cadena=ch

            ch=self.fl.siguiente()

            #leer entrada hasta que no sea un caracter valido de un identificador
            while ord(ch) in self.letra_minus or ord(ch) in self.letra_mayus or ord(ch) in self.numero:
                cadena += ch
                ch=self.fl.siguiente()
            
            #devolver el ultimo caracter a la entrada
            self.fl.devuelve(ch)

            # Comprobar si es un identificador o PR y devolver el objeto correspondiente
            if cadena in self.PR:
                return componentes.PR(cadena, self.nlinea)
            else:
                return componentes.Identif(cadena, self.nlinea)
            
        # Compruebo si el caracter es un numero
        elif ord(ch) in self.numero:

            punto=False
            num=ch

            ch=self.fl.siguiente()

            # Leer todos los elementos que forman el numero 
            while ord(ch) in self.numero: 
                num += ch
                ch=self.fl.siguiente()

            # Si leo un punto, entonces sera un numero real
            if ch==".":
                punto=True
                num += ch
                ch=self.fl.siguiente()
                while ord(ch) in self.numero: 
                    num += ch
                    ch=self.fl.siguiente()
            
            self.fl.devuelve(ch)

            # Devolver un objeto de la categoria correspondiente    
            if punto :
                return componentes.Numero(float(num),self.nlinea,'float')
            else:
                return componentes.Numero(int(num),self.nlinea,'int')
            
            
        elif ch== "\n":
            #incrementa el numero de linea ya que acabamos de saltar a otra
            # devolver el siguiente componente encontrado
            self.nlinea+=1
            return self.Analiza()

        else:
            return self.Analiza()
        
    

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
    

    
