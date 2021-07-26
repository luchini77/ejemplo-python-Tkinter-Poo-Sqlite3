class Empleado:
    
    def __init__(self, nombre, cargo, salario):
        self.__nombre = nombre
        self.__cargo = cargo
        self.__salario = salario


    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre


    @property
    def cargo(self):
        return self.__cargo

    @cargo.setter
    def cargo(self, cargo):
        self.__cargo = cargo


    @property
    def salario(self):
        return self.__salario

    @salario.setter
    def salario(self, salario):
        self.__salario = salario 
