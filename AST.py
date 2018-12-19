# -*- coding: latin-1 -*-

import sys

class AST:
  ids={}  # tabla de simbolos

  def __str__(self):
    return self.arbol()

  def actualiza_ids(self, id, contenido):  #actualiza la tabla de simbolos

    # Comprobacion semantica 1: Dos identificadores no pueden tener el mismo nombre
    if id not in self.ids:
      self.ids[id]=contenido
      return True

    else:
      print 'Error semantico: El identificador ya se ha declarado previamente'
      return False



class NodoAsignacion(AST):
  def __init__(self, izda, exp, linea):
    self.izda= izda
    self.exp= exp
    self.linea= linea

  def compsemanticas(self):
    # Comprobacion semantica adicional: El tipo de la variable debe ser igual al del contenido
    if self.izda.tipo != self.exp.tipo:
      print 'Error semantico (linea: ',self.linea,'): El tipo de la variable debe ser igual al del contenido. ',self.izda.tipo,'!=',self.exp.tipo
      return False

    else: 
      return True

  def arbol(self):
    return '( "Asignacion"\n  "linea: %d" \n%s\n%s\n)' % (self.linea, self.izda, self.exp)


class NodoSi(AST):
  def __init__(self, cond, si, sino, linea):
    self.cond= cond
    self.si= si
    self.sino= sino
    self.linea= linea

  def compsemanticas(self):
    pass

  def arbol(self):
    return '( "Si" "linea: %d" %s\n %s\n %s\n )' % (self.linea, self.cond, self.si, self.sino)


class NodoMientras(AST):
  def __init__(self, cond, exp):
    self.cond= cond
    self.exp= exp

  def compsemanticas(self):
    pass

  def arbol(self):
    return '( "Mientras" %s\n %s\n )' % (self.cond, self.exp)


class NodoLee(AST):
  def __init__(self, exp, linea):
    self.exp= exp
    self.linea= linea

  def compsemanticas(self):
    self.exp.compsemanticas()

    # Comprobacion semantica 7: En la instruccion LEE el argumento debe ser ENTERO o REAL
    if self.ids[self.exp.var].tipo=='ENTERO' or self.ids[self.exp.var].tipo=='REAL':
      return True
    else:
      print 'Error semantico (linea: ',self.linea,'): En la instruccion LEE el argumento debe ser ENTERO o REAL'
      return False

  def arbol(self):
    return '( "Lee" "linea: %d" %s )' % (self.linea, self.exp)


class NodoEscribe(AST):
  def __init__(self, exp, linea):
    self.exp= exp
    self.linea= linea

  def compsemanticas(self):
    pass

  def arbol(self):
    return '( "Escribe" "linea: %d" %s )' % (self.linea, self.exp)


class NodoCompuesta(AST):
  def __init__(self, sentencias, linea):
    self.sentencias= sentencias
    self.linea= linea

  def compsemanticas(self):
    for sent in self.sentencias:
      sent.compsemanticas()

  def arbol(self):
    r= ""
    for sent in self.sentencias:
      r+= sent.arbol()+"\n"
    return '( "Compuesta"\n %s)' % r


class NodoComparacion(AST):
  def __init__(self, op, izdo, dcho, linea):
    self.op= op
    self.izdo= izdo
    self.dcho= dcho
    self.linea= linea

  def compsemanticas(self):
    pass

  def arbol(self):
    return '( "Comparacion" "op: %s" "linea: %d" \n %s\n %s\n)' % \
           (self.op, self.linea, self.izdo, self.dcho)


class NodoAritmetica(AST):
  def __init__(self, op, izdo, dcho, linea):
    self.op= op
    self.izdo= izdo
    self.dcho= dcho
    self.linea= linea
    self.tipo='ENTERO'

  def compsemanticas(self):
    if self.izdo.tipo == self.dcho.tipo:
      self.tipo = self.dcho.tipo
    else:
      self.tipo='REAL'
    return True

  def arbol(self):
    return '( "Aritmetica" "op: %s" "tipo: %s" "linea: %d" \n %s\n %s\n)' % \
           (self.op, self.tipo, self.linea, self.izdo, self.dcho)


class NodoEntero(AST):
  def __init__(self, valor, linea):
    self.valor= valor
    self.linea= linea
    self.tipo= 'ENTERO'
    self.compsemanticas()

  def compsemanticas(self):
    # Comprobacion semantica 3: Conversion de enteros a reales
    self.valor = float(self.valor)

  def arbol(self):
    return '( "Entero" "valor: %s" "tipo: %s" "linea: %d" )' % (self.valor, self.tipo, self.linea)


class NodoReal(AST):
  def __init__(self, valor, linea):
    self.valor= valor
    self.linea= linea
    self.tipo= 'REAL'

  def compsemanticas(self):
    pass

  def arbol(self):
    return '( "Real" "valor: %s" "tipo: %s" "linea: %d" )' % (self.valor, self.tipo, self.linea)


class NodoBooleano(AST):
  def __init__(self, valor, linea):
    self.valor= valor
    self.linea= linea
    self.tipo= ''

  def compsemanticas(self):
    if self.valor==0:
      self.tipo= 'FALSO'
    else:
      self.tipo= 'CIERTO'

  def arbol(self):
    return '( "Booleano" "valor: %s" "tipo: %s" "linea: %d" )' % (self.valor, self.tipo, self.linea)


class NodoAccesoVariable(AST):
  def __init__(self, var, linea):
    self.var= var
    self.linea= linea
    self.tipo=''

  def compsemanticas(self):
    # Comprobacion semantica adicional: El identificador debe estar declarado previamente antes de usarlo
    if self.var not in self.ids:
      print 'Error semantico (linea: ',self.linea,'): El identificador debe estar declarado previamente antes de usarlo'
      return False

    else:
      self.tipo= self.ids[self.var].tipo
      return True

  def arbol(self):
    return '( "AccesoVariable" "nombre: %s" "linea: %d" )' % (self.var, self.linea)


class NodoAccesoVector(AST):
  def __init__(self, izda, posicion, exp, linea):
    self.izda= izda
    self.posicion= posicion
    self.exp= exp
    self.linea= linea
    self.tipo= izda.tipo

  def compsemanticas(self):
    # Comprobacion semantica adicional: El tipo del vector debe ser igual al del contenido
    if self.tipo != self.exp.tipo:
      print 'Error semantico (linea: ',self.linea,'): El tipo del vector debe ser igual al del contenido. ',self.tipo,'!=',self.exp.tipo
      return False

    # Comprobacion semantica 6: El numero debe estar en el rango del vector
    if self.posicion < 0 or self.posicion >= self.ids[self.izda.var].tamvector:
      print 'Error semantico (linea: ',self.linea,'): Se intenta acceder a una posicion que esta fuera del rango del vector. Tamano del vector = ',self.ids[self.izda.var].tamvector
      return False

    return True

  def arbol(self):
    return '( "AccesoVector" "tipo: %s" "posicion: %d" "linea: %d" %s\n %s\n)' % (self.tipo, self.posicion, self.linea, self.izda, self.exp)


class NodoVacio(AST):
  def __init__(self, linea):
    self.linea= linea

  def compsemanticas(self):
    #self.tipo= tipos.Error
    pass

  def arbol(self):
    return '( "NodoVacio" "linea: %d" )' % self.linea
