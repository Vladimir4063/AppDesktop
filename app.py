from collections import namedtuple
from sqlite3.dbapi2 import Row
from tkinter import ttk
from tkinter import *

#modulo de conexion
import sqlite3

class Product:

    db_name = 'database.db'
    
    def __init__(self, window):
        self.wind = window
        self.wind.title('Products Aplication')

        #Creating a frame Container
        frame = LabelFrame(self.wind, text= "Register a new Product")
        frame.grid(row=0, column=0, columnspan= 3, pady= 20) #relleno

        #name input
        Label(frame, text= 'Name: ').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        #price input 
        Label(frame, text='Price').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        #Button add product
        ttk.Button(frame, text='Save product', command= self.add_product).grid(row=3, columnspan=2, sticky= W + E)

        #Output Messages
        self.message = Label(text= '', fg='red')
        self.message.grid(row= 3 , column= 0, columnspan=2, sticky= W + E)

        #Table - dos grillas
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)

            #encabezados/text para las grillas
        self.tree.heading('#0', text='Name', anchor = CENTER) #Centramos el texto.
        self.tree.heading('#1', text='Price', anchor = CENTER)

        #Buttons / Botones
        ttk.Button(text= 'DELETE', command= self.delete_product).grid(row=5, column= 0, sticky= W + E)
        ttk.Button(text='EDIT', command= self.edit_product).grid(row=5, column=1, sticky=W + E)
        # filling the row / llenando las filas
        self.get_products() #llamo los productos de la bbdd
        

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters) #
            conn.commit()  # run - Ejecutamos la consulta sql
        return result

    def get_products(self):
        #cleaning table
        records = self.tree.get_children() #children: trae todos los datos
        for element in records:
            self.tree.delete(element)

        #quering data
        query ='SELECT * FROM product ORDER BY name DESC' # Ordenalos de forma descendente
        db_rows = self.run_query(query) #filas de la base de datos

        #filling data
        for row in db_rows:
            self.tree.insert('', 0, text= row[1], values= row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0 #lectura del input


    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES (NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Product {} added Successfully'.format(self.name.get()) #imprimos mensaje de guardado con nombre de producto
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = "Name and price required"
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except Exception as ex:
            self.message['text'] = 'Please Select a Record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except Exception as ex:
            self.message['text'] = 'Please Select a Record'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Product'

        #Old name
        Label(self.edit_wind, text= 'Old name').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value= name), state='readonly').grid(row=0, column=2)

        #New name
        Label(self.edit_wind, text= 'New name').grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        #Old price
        Label(self.edit_wind, text= ' Old price').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_price), state= 'readonly').grid(row=2, column=2) # traemos el valor de la variable (StrinVar) PRICE
        

        #New price
        Label(self.edit_wind, text= 'New price').grid(row=3, column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)

        Button(self.edit_wind, text='Update', command= lambda:self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row=4, column=2, sticky= W)

    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated Successfully'.format(name)
        self.get_products()

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
