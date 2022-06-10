from Programs import *

TOKEN_DEFINIR = "DEFINIR"
TOKEN_PROGRAMA = "PROGRAMA"
TOKEN_INTERPRETE = "INTERPRETE"
TOKEN_TRADUCTOR = "TRADUCTOR"
TOKEN_EJECUTABLE = "EJECUTABLE"
TOKEN_SALIR = "SALIR"

ejecutador : Ejecutor = Ejecutor()
run : bool = True

def simulator_usage():
    print("Uso:\n\tDEFINIR [TIPO] [ARGUMENTOS]")
    print("\tCrea una estructura del tipo [TIPO] con sus argumentos")

    print("\tTIPOS PERMITIDOS:")
    print("\t\t-PROGRAMA [NOMBRE] [LENGUAJE BASE]")
    print("\t\tPrograma con nombre [NOMBRE] escrito en [LENGUAJE BASE]")
    print("\t\t\t-NOMBRE : Nombre del programa a crear")
    print("\t\t\t-LENGUAJE BASE : Lenguaje en el que esta escrito el programa")

    print("\t\t-INTERPRETE [LENGUAJE BASE] [LENGUAJE]")
    print("\t\tInterprete de [LENGUAJE] escrito en [LENGUAJE BASE]")
    print("\t\t\t-LENGUAJE BASE : Lenguaje en el que esta escrito el interprete")
    print("\t\t\t-LENGUAJE : Lenguaje que interpreta")

    print("\t\t-TRADUCTOR [LENGUAJE BASE] [LENGUAJE ORIGEN] [LENGUAJE DESTINO]")
    print("\t\tTraductor de [LENGUAJE ORIGEN] a [LENGUAJE DESTINO] escrito en [LENGUAJE BASE]")
    print("\t\t\t-LENGUAJE BASE : Lenguaje en el que esta escrito el traductor")
    print("\t\t\t-LENGUAJE ORIGEN : Lenguaje del que se traduce")
    print("\t\t\t-LENGUAJE DESTINO : Lenguaje al que se traduce")

    print("\n\tEJECUTABLE [NOMBRE]\n\tIntenta ejecutar el programa [NOMBRE].")
    print("\t\t-NOMBRE : Nombre del programa a intentar ejecutar")

    print("\n\tSALIR\n\tMata\\sale del programa.")


def wrong_params():
    print("Parametro invalido o numero de parametros incorrecto.")
    simulator_usage()


while (run):
    tokens : List[str] = input("Introduce un comando>").split()
    if (len(tokens) == 0):
        print("Comando no valido.")
        continue

    comando : str = tokens.pop(0).upper()
    if (comando == TOKEN_DEFINIR):
        if (len(tokens) == 0):
            wrong_params()
            continue

        tipo : str = tokens.pop(0).upper()
        if (tipo == TOKEN_PROGRAMA):
            if (len(tokens) != 2):
                wrong_params()
                continue
            ejecutador.define_program(tokens[0], tokens[1])
        elif (tipo == TOKEN_INTERPRETE):
            if (len(tokens) != 2):
                wrong_params()
                continue
            ejecutador.define_interpreter(tokens[0], tokens[1])
        elif (tipo == TOKEN_TRADUCTOR):
            if (len(tokens) != 3):
                wrong_params()
                continue
            ejecutador.define_traductor(tokens[0], tokens[1], tokens[2])
        else:
            print("Estructura a definir invalida.")
            simulator_usage()
    elif (comando == TOKEN_EJECUTABLE):
        if (len(tokens) != 1):
            wrong_params()
            continue
        ejecutador.execute_program(tokens.pop(0))
    elif (comando == TOKEN_SALIR):
        run = False
    else:
        print("Comando invalido.")
        simulator_usage()

"""
ejecutador.define_program("fibo", LOCAL_LANG)
ejecutador.execute_program("fibo")
ejecutador.define_program("factorial", "Java")
ejecutador.execute_program("factorial")
ejecutador.define_interpreter("c", "Java")
ejecutador.execute_program("factorial")
ejecutador.define_interpreter(LOCAL_LANG, "c")
ejecutador.execute_program("factorial")
ejecutador.define_program("holamundo", "Python3")
ejecutador.define_traductor("wtf42", "Python3", LOCAL_LANG)
ejecutador.execute_program("holamundo")
ejecutador.define_traductor("c", "wtf42", "Java")
ejecutador.execute_program("holamundo")
"""