# -*- coding: latin-1 -*-

import sys

class AST:
  def __str__(self):
    return self.arbol()

class NodoAsignacion(AST):
  def __init__(self, izda, exp, linea):
    self.izda= izda
    self.exp= exp
    self.linea= linea

  def compsemanticas(self):
    self.izda.compsemanticas()
    self.exp.compsemanticas()
    """if not tipos.igualOError(self.izda.tipo, self.exp.tipo):
      errores.semantico("Tipos incompatibles en asignacion (%s y %s)." %
                        (self.izda.tipo, self.exp.tipo), self.linea)
    else:
      if not self.izda.tipo.elemental() or not self.exp.tipo.elemental():
        errores.semantico("Solo puedo asignar objetos de tipos elementales.", self.linea)"""

  def arbol(self):
    return '( "Asignacion"\n  "linea: %d" \n%s\n%s\n)' % (self.linea, self.izda, self.exp)

class NodoDevuelve(AST):
  def __init__(self, exp, f, linea):
    self.exp= exp
    self.f= f
    self.linea= linea

  def compsemanticas(self):
    self.exp.compsemanticas()
    """if not tipos.igualOError(self.exp.tipo, self.f.tipoDevuelto):
      errores.semantico("El tipo de la expresion del devuelve debe coincidir con el de la funcion.", self.linea)"""

  def arbol(self):
    return '( "Devuelve" "linea: %d" %s)' % (self.linea, self.exp)

class NodoSi(AST):
  def __init__(self, cond, si, sino, linea):
    self.cond= cond
    self.si= si
    self.sino= sino
    self.linea= linea

  def compsemanticas(self):
    self.cond.compsemanticas()
    self.si.compsemanticas()
    self.sino.compsemanticas()
    """if not tipos.igualOError(self.cond.tipo, tipos.Logico):
      errores.semantico("La condicion del si debe ser de tipo logico.", self.linea)"""

  def arbol(self):
    return '( "Si" "linea: %d" %s\n %s\n %s\n )' % (self.linea, self.cond, self.si, self.sino)

class NodoMientras(AST):
  def __init__(self, cond, exp):
    self.cond= cond
    self.exp= exp

  def compsemanticas(self):
    self.exp.compsemanticas()
    """if self.exp.tipo!= tipos.Error:
      if self.exp.tipo!= tipos.Entero and self.exp.tipo!= tipos.Cadena:
        errores.semantico("Solo se escribir enteros y cadenas.", self.linea)"""

  def arbol(self):
    return '( "Mientras" %s\n %s\n )' % (self.cond, self.exp)

class NodoLee(AST):
  def __init__(self, exp, linea):
    self.exp= exp
    self.linea= linea

  def compsemanticas(self):
    self.exp.compsemanticas()
    """if self.exp.tipo!= tipos.Error:
      if self.exp.tipo!= tipos.Entero and self.exp.tipo!= tipos.Cadena:
        errores.semantico("Solo se escribir enteros y cadenas.", self.linea)"""

  def arbol(self):
    return '( "Lee" "linea: %d" %s )' % (self.linea, self.exp)

class NodoEscribe(AST):
  def __init__(self, exp, linea):
    self.exp= exp
    self.linea= linea

  def compsemanticas(self):
    self.exp.compsemanticas()
    """if self.exp.tipo!= tipos.Error:
      if self.exp.tipo!= tipos.Entero and self.exp.tipo!= tipos.Cadena:
        errores.semantico("Solo se escribir enteros y cadenas.", self.linea)"""

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
    self.izdo.compsemanticas()
    self.dcho.compsemanticas()
    """if not tipos.igualOError(self.izdo.tipo, tipos.Entero) or \
       not tipos.igualOError(self.dcho.tipo, tipos.Entero):
      errores.semantico("Las operaciones de comparacion solo pueden operar con enteros.", self.linea)
      self.tipo= tipos.Error
    else:
      self.tipo= tipos.Logico"""

  def arbol(self):
    return '( "Comparacion" "op: %s" "linea: %d" \n %s\n %s\n)' % \
           (self.op, self.linea, self.izdo, self.dcho)

class NodoAritmetica(AST):
  def __init__(self, op, izdo, dcho, linea):
    self.op= op
    self.izdo= izdo
    self.dcho= dcho
    self.linea= linea
    self.tipo='REAL'

  def compsemanticas(self):
    self.izdo.compsemanticas()
    self.dcho.compsemanticas()
    """if not tipos.igualOError(self.izdo.tipo, tipos.Entero) or \
       not tipos.igualOError(self.dcho.tipo, tipos.Entero):
      errores.semantico("Las operaciones aritmeticas solo pueden operar con enteros.", self.linea)
      self.tipo= tipos.Error
    else:
      self.tipo= tipos.Entero"""

  def arbol(self):
    return '( "Aritmetica" "op: %s" "tipo: %s" "linea: %d" \n %s\n %s\n)' % \
           (self.op, self.tipo, self.linea, self.izdo, self.dcho)

class NodoEntero(AST):
  def __init__(self, valor, linea):
    self.valor= valor
    self.linea= linea
    self.tipo= 'ENTERO'

  def compsemanticas(self):
    self.tipo= 'ENTERO'

  def arbol(self):
    return '( "Entero" "valor: %s" "tipo: %s" "linea: %d" )' % (self.valor, self.tipo, self.linea)

class NodoReal(AST):
  def __init__(self, valor, linea):
    self.valor= valor
    self.linea= linea
    self.tipo= 'REAL'

  def compsemanticas(self):
    self.tipo= 'REAL'

  def arbol(self):
    return '( "Real" "valor: %s" "tipo: %s" "linea: %d" )' % (self.valor, self.tipo, self.linea)

class NodoCadena(AST):
  def __init__(self, cad, linea):
    self.cad= cad
    self.linea= linea

  def compsemanticas(self):
    #self.tipo= tipos.Cadena
    pass

  def arbol(self):
    return '( "Cadena" "valor: %s" "tipo: %s" "linea: %d" )' % (str(self.cad)[1:-1], self.tipo, self.linea)

class NodoLlamada(AST):
  def __init__(self, f, args, linea):
    self.f= f
    self.args= args
    self.linea= linea

  def compsemanticas(self):
    for arg in self.args:
      arg.compsemanticas()
    """if not self.f.tipo== tipos.Funcion:
      errores.semantico("Estas intentando llamar a algo que no es una funcion.",
                        self.linea)
      self.tipo= tipos.Error
      return
    self.tipo= self.f.tipoDevuelto
    if self.f.tipoDevuelto== tipos.Error:
      return
    if len(self.args)!= len(self.f.parametros):
      errores.semantico("La llamada a %s deberia tener %d parametros en lugar de %d." %
                        (self.f.id, len(self.f.parametros), len(self.args)), self.linea)
    else:
      for i in range(len(self.args)):
        arg= self.args[i]
        pf= self.f.parametros[i]
        if not tipos.igualOError(arg.tipo, pf.tipo):
          errores.semantico("No coincide el tipo del parametro %d (deberia ser %s)." %
                            (i+1, pf.tipo), self.linea)"""

  def arbol(self):
    l= []
    for p in self.args:
      l.append(p.arbol())
    return '("Llamada" "f: %s" "tipo: %s" "linea: %d" %s )' % (self.f, self.tipo, self.linea, "\n".join(l))

class NodoAccesoVariable(AST):
  def __init__(self, var, linea):
    self.var= var
    self.linea= linea

  def compsemanticas(self):
    #self.tipo= self.var.tipo
    pass

  def arbol(self):
    return '( "AccesoVariable" "nombre: %s" "linea: %d" )' % (self.var, self.linea)

class NodoAccesoVector(AST):
  def __init__(self, izda, exp, linea):
    self.izda= izda
    self.exp= exp
    self.linea= linea
    self.tipo= 'ENTERO'

  def compsemanticas(self):
    self.izda.compsemanticas()
    self.exp.compsemanticas()
    """if self.izda.tipo!= tipos.Error:
      if self.izda.tipo.elemental():
        errores.semantico("Estas accediendo a una expresion de tipo %s como si fuera un vector." %
                          self.izda.tipo, self.linea)
        self.tipo= tipos.Error
      elif self.izda.tipo== tipos.Funcion:
        errores.semantico("Estas accediendo a la funcion %s como si fuera un vector." %
                          self.izda.var.id, self.linea)
        self.tipo= tipos.Error
      else:
        self.tipo= self.izda.tipo.base
    else:
      self.tipo= tipos.Error
    if not tipos.igualOError(self.exp.tipo, tipos.Entero):
      errores.semantico("El tipo de la expresion de acceso al vector debe ser entero.",
                        self.linea)"""

  def arbol(self):
    return '( "AccesoVector" "tipo: %s" "linea: %d" %s\n %s\n)' % (self.tipo, self.linea, self.izda, self.exp)

class NodoVacio(AST):
  def __init__(self, linea):
    self.linea= linea

  def compsemanticas(self):
    #self.tipo= tipos.Error
    pass

  def arbol(self):
    return '( "NodoVacio" "linea: %d" )' % self.linea
