from __future__ import annotations
from operator import contains
from typing import Dict, List, Set

LOCAL_LANG : str = "LOCAL"

class Ejecutor:

    def __init__(self : Ejecutor) -> None:
        self.languages : Dict[str, NodoLenguaje] = {LOCAL_LANG : NodoLenguaje(LOCAL_LANG)}

        self.programs : Dict[str, Programa] = {}
        self.interp : Dict[str, List[Interprete]] = {}
        self.trad : Dict[str, List[Traductor]] = {}

        self.wayToLocal : Dict[str, bool] = {LOCAL_LANG : True}
        self.toApply : List[ProgramaBase] = []

    
    def can_be_executed(self : Ejecutor, lang : str) -> bool:
        return contains(self.languages, lang) and self.wayToLocal[lang]
    

    def apply_interp(self : Ejecutor, interp : Interprete) -> bool:
        if (not self.can_be_executed(interp.baseLanguage)):
            return False
        
        self.languages[interp.targetLanguage].add_neighboor(self.languages[interp.baseLanguage])
        return True

    
    def apply_trad(self : Ejecutor, trad : Traductor) -> bool:
        if (not self.can_be_executed(trad.baseLanguage)):
            return False

        self.languages[trad.fromLanguage].add_neighboor(self.languages[trad.toLanguage])
        return True


    def update_lang_routes(self : Ejecutor) -> None:
        for l in self.languages.keys():
            if (self.wayToLocal[l]):
                continue
            
            if (self.try_reaching_local(l)):
                self.wayToLocal[l] = True

    def apply_int_trad(self : Ejecutor) -> None:
        remove : bool = False
        changed : bool = True
        
        while (changed):
            i : int = 0
            changed = False
            while (i < len(self.toApply)):
                p : ProgramaBase = self.toApply[i]
                assert (not isinstance(p, Programa))

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
        if (not contains(self.programs, program)):
            print("El programa %s no existe. Revise el case del programa."%(program))
            return False
        
        p : Programa = self.programs[program]
        if (self.wayToLocal[p.baseLanguage]):
            print("El programa es ejecutado con exito!")
            return True
        
        print("El programa no puede ser ejecutado con exito! Ha escapado.")
        return False


class NodoLenguaje:

    def __init__(self : NodoLenguaje, language : str) -> None:
        self.language : str = language
        self.adj : List[NodoLenguaje] = []


    def add_neighboor(self : NodoLenguaje, neighboor : NodoLenguaje) -> None:
        if (neighboor in self.adj):
            return

        self.adj.append(neighboor)
    

class ProgramaBase:

    def __init__(self : ProgramaBase, baseLanguage : str) -> None:
        self.baseLanguage = baseLanguage


class Programa(ProgramaBase):

    def __init__(self : Programa, baseLanguage : str, name : str) -> None:
        super().__init__(baseLanguage)
        self.name = name


class Interprete(ProgramaBase):

    def __init__(self : Interprete, baseLanguage : str, targetLanguage :str) -> None:
        super().__init__(baseLanguage)
        self.targetLanguage = targetLanguage


class Traductor(ProgramaBase):

    def __init__(self : Traductor, baseLanguage : str, fromLanguage : str, toLanguage :str) -> None:
        super().__init__(baseLanguage)
        self.fromLanguage = fromLanguage
        self.toLanguage = toLanguage