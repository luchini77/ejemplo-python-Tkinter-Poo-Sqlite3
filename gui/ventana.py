from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import re
from modelos.verificar_datos import Validacion
from modelos.empleados import Empleado
from datos.conexion import DB


validar = Validacion()
db = DB()

class Ventana(Tk):


    def __init__(self):
        super().__init__()

        self.inicializar_gui()
        self.llenar_datos()
        self.habilitar_cajas('disabled')
        self.habilitar_botones_sql('normal')
        self.habilitar_botones_guardar('disabled')
        self.id = -1


    def inicializar_gui(self):
        self.title('Aplicacion CRUD Empleados.')

        self.mi_nombre = StringVar()
        self.mi_cargo = StringVar()
        self.mi_salario = StringVar()

        
        #FRAME
        marco = LabelFrame(self, text="Nomina Empleados")
        marco.pack()

        marco1 = Frame(self)
        marco1.pack()

        marco2 = Frame(self)
        marco2.pack()

        marco3 = Frame(self)
        marco3.pack()

        # LABEL

        nombre_label = Label(marco, text='Nombre:')
        nombre_label.grid(row=0, column=0, padx=10, pady=10)

        cargo_label = Label(marco,text='Cargo:')
        cargo_label.grid(row=1, column=0, padx=10, pady=10)

        salario_label = Label(marco, text='Salario:')
        salario_label.grid(row=2, column=0, padx=10, pady=10)

        #ENTRY

        self.txt_nombre = Entry(marco, textvariable=self.mi_nombre)
        self.txt_nombre.grid(row=0, column=1, padx=10, pady=10)

        self.txt_cargo = Entry(marco, textvariable=self.mi_cargo)
        self.txt_cargo.grid(row=1, column=1, padx=10, pady=10)

        self.txt_salario = Entry(marco, textvariable=self.mi_salario)
        self.txt_salario.grid(row=2, column=1, padx=10, pady=10)

        #BOTONES
        self.btn_nuevo = Button(marco, text='Nuevo',width=7, command=self.nuevo)
        self.btn_nuevo.grid(row=0,column=3,padx=5,pady=5)

        self.btn_modificar = Button(marco, text='Actualizar', command=self.modificar)
        self.btn_modificar.grid(row=1,column=3,padx=5,pady=5)

        self.btn_borrar = Button(marco, text='Borrar',width=7, command=self.borrar)
        self.btn_borrar.grid(row=2,column=3,padx=5,pady=5)


        #GRILLA
        self.grid = ttk.Treeview(marco2, columns=('col1','col2','col3'))

        self.grid.column('#0',width=50)
        self.grid.column('col1',width=130,anchor=CENTER)
        self.grid.column('col2',width=100,anchor=CENTER)
        self.grid.column('col3',width=100,anchor=CENTER)

        self.grid.heading('#0',text='Id',anchor=CENTER)
        self.grid.heading('col1',text='NOMBRE',anchor=CENTER)
        self.grid.heading('col2',text='CARGO',anchor=CENTER)
        self.grid.heading('col3',text='SALARIO',anchor=CENTER)

        self.grid.pack(side=LEFT,fill = Y)

        sb = Scrollbar(marco2, orient=VERTICAL)
        sb.pack(side=RIGHT, fill= Y)
        self.grid.config(yscrollcommand= sb.set)
        sb.config(command=self.grid.yview)

        self.grid['selectmode'] = 'browse'

        #BOTONES GUARDAR Y SALIR
        self.btn_guardar = Button(marco3, text='Guardar', command=self.guardar)
        self.btn_guardar.grid(row=0,column=0,padx=5,pady=5)

        self.btn_cancelar = Button(marco3, text='Cancelar', command=self.cancelar)
        self.btn_cancelar.grid(row=0,column=1,padx=5,pady=5)


    #METODOS AYUDA
    def habilitar_cajas(self, estado):
        self.txt_nombre.configure(state=estado)
        self.txt_cargo.configure(state=estado)
        self.txt_salario.configure(state=estado)


    def limpiar_cajas(self):
        self.txt_nombre.delete(0,END)
        self.txt_cargo.delete(0,END)
        self.txt_salario.delete(0,END)


    def habilitar_botones_sql(self, estado):
        self.btn_nuevo.configure(state=estado)
        self.btn_modificar.configure(state=estado)
        self.btn_borrar.configure(state=estado)


    def habilitar_botones_guardar(self, estado):
        self.btn_guardar.configure(state=estado)
        self.btn_cancelar.configure(state=estado)


    
    def nuevo(self):
        self.habilitar_cajas('normal')
        self.habilitar_botones_sql('disabled')
        self.habilitar_botones_guardar('normal')
        self.limpiar_cajas()
        self.txt_nombre.focus()
        

    def cancelar(self):
        r = messagebox.askquestion('Cancelar','Esta seguro que desea cancelar la operación actual.')

        if r == messagebox.YES:
            self.limpiar_cajas()
            self.habilitar_botones_guardar(DISABLED)
            self.habilitar_botones_sql(NORMAL)
            self.habilitar_cajas(DISABLED)


    def limpia_grid(self):
        for item in self.grid.get_children():
            self.grid.delete(item)


    #METODOS CRUD
    def guardar(self):
        nombre = self.mi_nombre.get().strip()
        nombre_valido = validar.validar_nombre(nombre)

        cargo = self.mi_cargo.get().strip()
        cargo_valido = validar.validar_cargo(cargo)

        salario = self.mi_salario.get().strip()
        salario_valido = validar.validar_salario(salario)


        if nombre_valido == True and cargo_valido == True and salario_valido == True:
    
            empleado = Empleado(nombre, cargo, salario)

            if self.id == -1:
    
                sql = "INSERT INTO empleado (nombre,cargo,salario) VALUES(?,?,?)"
                parametros = (empleado.nombre,empleado.cargo,empleado.salario)

                db.ejecutar_consulta(sql,parametros)

                messagebox.showinfo('INSERTAR','Empleado guardado correctamente.')

            else:

                sql = "UPDATE empleado SET nombre=?,cargo=?,salario=? WHERE id_empleado=?"
                parametros = (empleado.nombre,empleado.cargo,empleado.salario,self.id)

                db.ejecutar_consulta(sql, parametros)

                messagebox.showinfo('ACTUALIZAR','Elemento modificado correctamente.')
                self.idx = -1

        else:
            messagebox.showerror('Mensaje','Error, al guardar el empleado.')
        
        self.limpia_grid()
        self.llenar_datos()
        self.limpiar_cajas()
        self.txt_nombre.focus()
        self.habilitar_botones_guardar(DISABLED)
        self.habilitar_botones_sql(NORMAL)
        self.habilitar_cajas(DISABLED)


    def llenar_datos(self):

        sql = 'SELECT * FROM empleado'
        
        resultado = db.ejecutar_consulta(sql)

        for i in resultado:
            self.grid.insert('',END, text=i[0], values=(i[1],i[2],i[3]))

        if len(self.grid.get_children()) > 0:
            self.grid.selection_set(self.grid.get_children()[0])


    def modificar(self):

        selecion = self.grid.focus()
        clave = self.grid.item(selecion, 'text')

        if clave == '':
            messagebox.showwarning('MODIFICAR','Debes seleccionar un elemento.')

        else:

            self.id = clave

            self.habilitar_cajas('normal')

            valores = self.grid.item(selecion, 'values')

            self.limpiar_cajas()

            self.txt_nombre.insert(0, valores[0])
            self.txt_cargo.insert(0, valores[1])
            self.txt_salario.insert(0, valores[2])

            self.habilitar_botones_sql('disabled')
            self.habilitar_botones_guardar('normal')
            self.txt_nombre.focus()


    def borrar(self):
        selecion = self.grid.focus()
        clave = self.grid.item(selecion, 'text')

        if clave == '':
            messagebox.showwarning('ELIMINAR','Debes seleccionar un elemento.')

        else:

            self.id = clave

            respuesta = messagebox.askquestion('ELIMINAR','Desea eliminar el registro selecciónado.')

            if respuesta == messagebox.YES:
                sql = "DELETE FROM empleado WHERE id_empleado=?"
                parametros = (self.id,)

                db.ejecutar_consulta(sql,parametros)

                messagebox.showinfo('Eliminar','Elemento eliminado correctamente.')
                self.limpia_grid()
                self.llenar_datos()
            else:
                messagebox.showwarning('Eliminar', 'No fue posible eliminar el elemento.')