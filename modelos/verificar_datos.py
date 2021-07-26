import re
from tkinter import messagebox



class Validacion:

    def __init__(self):
        pass


    def validar_nombre(self, nombre):

        if nombre.isalpha() and len(nombre) >= 3:
            return True
        else:
            return False

    def validar_cargo(self, cargo):

        if cargo.isalpha() and len(cargo) >= 4:
            return True
        else:
            return False

    def validar_salario(self, salario):

        if salario.isdigit() and int(salario) > 0:
            return True
        else:
            return False