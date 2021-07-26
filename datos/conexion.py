import sqlite3


database = "datos/empleados.db"

class DB:

    def __init__(self):
        pass


    def ejecutar_consulta(self, consulta, parametros = ()):

        with sqlite3.connect(database) as conn:
            self.cursor = conn.cursor()
            resultado = self.cursor.execute(consulta, parametros)
            conn.commit()
            return resultado