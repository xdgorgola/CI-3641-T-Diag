from __future__ import annotations
from operator import contains
from typing import Dict, List, Set

"""
Constante. Indica el nombre del lenguaje local de una maquina.
"""
LOCAL_LANG : str = "LOCAL"

class Ejecutor:
    """
    Se encarga de mantener la informacion de los programas, traductores einterpretes creados.

    Tiene un grafo dirigido donde cada vertice representa un lenguaje y cada lado si es posible 
    ejecutar ese lenguaje mediante otro (ya sea por una combinacion de traductores e interpretes).

    La solucion se basa en que el problema de ejecutar programas de un lenguaje, puede convertirse en 
    el problema de ejecutar un programa en otro lenguaje mediante cadenas de traductores e interpretes.
    """

    def __init__(self : Ejecutor) -> None:
        self.languages : Dict[str, NodoLenguaje] = {LOCAL_LANG : NodoLenguaje(LOCAL_LANG)}

        self.programs : Dict[str, Programa] = {}
        self.interp : Dict[str, List[Interprete]] = {}
        self.trad : Dict[str, List[Traductor]] = {}

        self.wayToLocal : Dict[str, bool] = {LOCAL_LANG : True}
        self.toApply : List[ProgramaBase] = []

    
    def can_be_executed(self : Ejecutor, lang : str) -> bool:
        """
        Indica si los programas de un lenguaje pueden ser ejecutados.

        Argumentos:
            lang -- Lenguaje a ver si es posible su ejecucion

        Returns:
            True si programas escritos en el lenguaje pueden ser ejecutados.
            False en caso contrario o si el lenguaje no existe en las tablas.
        """

        return contains(self.languages, lang) and self.wayToLocal[lang]
    

    def apply_interp(self : Ejecutor, interp : Interprete) -> bool:
        """
        Aplica los efectos de un interprete al grafo de lenguajes.

        Argumentos:
            interp -- Interprete a aplicar

        Returns:
            True si el interprete puede ser aplicado.
            False si el interprete no puede ser ejecutado.
        """

        if (not self.can_be_executed(interp.baseLanguage)):
            return False
        
        self.languages[interp.targetLanguage].add_neighboor(self.languages[interp.baseLanguage])
        return True

    
    def apply_trad(self : Ejecutor, trad : Traductor) -> bool:
        """
        Aplica los efectos de un traductor al grafo de lenguajes.

        Argumentos:
            interp -- traductor a aplicar

        Returns:
            True si el traductor puede ser aplicado.
            False si el traductor no puede ser ejecutado.
        """

        if (not self.can_be_executed(trad.baseLanguage)):
            return False

        self.languages[trad.fromLanguage].add_neighboor(self.languages[trad.toLanguage])
        return True


    def update_lang_routes(self : Ejecutor) -> None:
        """
        Actualiza la lista de lenguajes que pueden ser ejecutados intentando
        encontrar un camino hasta el lenguaje LOCAL desde cada lenguaje.
        """

        for l in self.languages.keys():
            if (self.wayToLocal[l]):
                continue
            
            if (self.try_reaching_local(l)):
                self.wayToLocal[l] = True


    def apply_int_trad(self : Ejecutor) -> None:
        """
        Intenta aplicar los interpretes y traductores que no han 
        sido aplicados aun al grafo de lenguajes y actualiza la 
        lista de lenguajes que pueden ejecutarse.
        """

        remove : bool = False
        changed : bool = True
        i : int = 0
        
        while (changed):
            i = 0
            changed = False
            while (i < len(self.toApply)):
                p : ProgramaBase = self.toApply[i]

                if (isinstance(p, Interprete)):
                    remove = self.apply_interp(p)
                elif (isinstance(p, Traductor)):
                    remove = self.apply_trad(p)

                if (remove):
                    self.toApply.pop(i)
                    self.update_lang_routes()
                    changed = True
                    i -= 1
        
                i += 1
    

    def try_reaching_local(self : Ejecutor, fromL : str) -> bool:
        """
        BFS que parte de un lenguaje e intenta encontrar un camino
        hasta el lenguaje LOCAL

        Argumentos:
            fromL -- Lenguaje de partida

        Returns:
            True si se encontro un camino hasta LOCAL
            Flase en otro caso
        """

        # BFS DE LA MUERTE. SEGURO EXPLOTA     
        visited : Set[str] = set({})
        next : List[NodoLenguaje] = [self.languages[fromL]]
        visited.add(self.languages[fromL])

        while (len(next) > 0):
            current : NodoLenguaje = next.pop()

            if (current.language == LOCAL_LANG):
                return True

            for v in current.adj:
                if (not (v in visited)):
                    visited.add(v)
                    next.append(v)

        return False


    def define_interpreter(self : Ejecutor, base : str, target : str) -> bool:
        """
        Crea un interprete, agrega las entradas necesarias a las 
        tablas e intenta aplicar los interpretes/traductores de la 
        lista de por aplicar.

        Argumentos:
            base -- Lenguaje en el que esta escrito
            target -- Lenguaje que se interpreta

        Returns:
            True si el interprete no existe y fue creado
            False si el interprete ya existe
        """

        if (not contains(self.languages, base)):
            self.languages[base] = NodoLenguaje(base)
            self.wayToLocal[base] = False
        
        if (not contains(self.languages, target)):
            self.languages[target] = NodoLenguaje(target)
            self.wayToLocal[target] = False

        if (not contains(self.interp, base)):
            self.interp[base] = []

        for i in self.interp[base]:
            if i.targetLanguage == target:
                print("El interpretador de %s escrito en %s ya existe."%(target, base))
                return False

        interp : Interprete = Interprete(base, target)
        self.toApply.append(interp)
        self.interp[base].append(interp)

        print("Creado el interpretador de %s escrito en %s."%(target, base))
        self.apply_int_trad()
        return True

    
    def define_traductor(self : Ejecutor, base : str, fromL : str, toL :str) -> bool:
        """
        Crea un traductor, agrega las entradas necesarias a las 
        tablas e intenta aplicar los interpretes/traductores de la 
        lista de por aplicar.

        Argumentos:
            base -- Lenguaje en el que esta escrito
            fromL -- Lenguaje desde el que se traduce
            toL -- Lenguaje al que se traduce

        Returns:
            True si el traductor no existe y fue creado
            False si el traductor ya existe
        """

        if (not contains(self.languages, base)):
            self.languages[base] = NodoLenguaje(base)
            self.wayToLocal[base] = False
        
        if (not contains(self.languages, fromL)):
            self.languages[fromL] = NodoLenguaje(fromL)
            self.wayToLocal[fromL] = False

        if (not contains(self.languages, toL)):
            self.languages[toL] = NodoLenguaje(fromL)
            self.wayToLocal[toL] = False

        if (not contains(self.trad, base)):
            self.trad[base] = []
        
        for t in self.trad[base]:
            if (t.fromLanguage == fromL and t.toLanguage == toL):
                print("El traductor de %s a %s escrito en %s ya existe." %(base, fromL, toL))
                return False
        
        trad : Traductor = Traductor(base, fromL, toL)
        self.toApply.append(trad)
        self.trad[base].append(trad)

        print("Creado el traductor de %s a %s escrito en %s."%(fromL, toL, base))
        self.apply_int_trad()
        return True
    
    
    def define_program(self : Ejecutor, name : str, base : str) -> bool:
        """
        Crea un programa, agrega las entradas necesarias a las 
        tablas.

        Argumentos:
            name -- Nombre del programa
            base -- Lenguaje en el que esta escrito

        Returns:
            True si el programa no existe y fue creado
            False si el programa ya existe
        """

        if (not contains(self.languages, base)):
            self.languages[base] = NodoLenguaje(base)
            self.wayToLocal[base] = False
        
        if (contains(self.programs, name)):
            print("El programa %s ya existe."%(name))
            return False

        prog : Programa = Programa(base, name)
        self.programs[name] = prog
        print("Creado el programa %s escrito en %s."%(name, base))
        return True
    

    def execute_program(self : Ejecutor, program : str) -> bool:
        """
        Intenta ejecutar un programa

        Argumentos:
            program -- Nombre del programa

        Returns:
            True si se puede ejecutar el programa
            False si no se puede
        """

        if (not contains(self.programs, program)):
            print("El programa %s no existe. Revise el case del programa."%(program))
            return False
        
        p : Programa = self.programs[program]
        if (self.wayToLocal[p.baseLanguage]):
            print("El programa es ejecutado con exito!")
            return True
        
        print("El programa no puede ser ejecutado con exito..")
        return False


class NodoLenguaje:
    """
    vertice de un grafo dirigido que representa un lenguaje.
    """

    def __init__(self : NodoLenguaje, language : str) -> None:
        self.language : str = language
        self.adj : List[NodoLenguaje] = []


    def add_neighboor(self : NodoLenguaje, neighboor : NodoLenguaje) -> None:
        """
        Agrega un lado hacia otro vertice

        Argumentos:
            neighboor -- Nuevo vertice adyacente
        """

        if (neighboor in self.adj):
            return

        self.adj.append(neighboor)
    

class ProgramaBase:
    """
    Clase abstracta base que representa un programa escrito en un lenguaje
    """

    def __init__(self : ProgramaBase, baseLanguage : str) -> None:
        self.baseLanguage = baseLanguage


class Programa(ProgramaBase):
    """
    Programa con un nombre y un lenguaje en el que fue escrito.
    """

    def __init__(self : Programa, baseLanguage : str, name : str) -> None:
        super().__init__(baseLanguage)
        self.name = name


class Interprete(ProgramaBase):
    """
    Interprete de un lenguaje escrito en otro
    """

    def __init__(self : Interprete, baseLanguage : str, targetLanguage :str) -> None:
        super().__init__(baseLanguage)
        self.targetLanguage = targetLanguage


class Traductor(ProgramaBase):
    """
    Traductor de un lenguaje a otro escrito en algun lenguaje
    """

    def __init__(self : Traductor, baseLanguage : str, fromLanguage : str, toLanguage :str) -> None:
        super().__init__(baseLanguage)
        self.fromLanguage = fromLanguage
        self.toLanguage = toLanguage