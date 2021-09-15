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

        #Table - dos grillas
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)

            #encabezados/text para las grillas
        self.tree.heading('#0', text='Name', anchor = CENTER) #Centramos el texto.
        self.tree.heading('#1', text='Price', anchor = CENTER)

        self.get_products() #llamo los productos de la bbdd
        

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters) #
            conn.commit()  # run - Ejecutamos la consulta sql
        return result

    def get_products(self):
        #cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        #quering data
        query ='SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)

        #filling data
        for row in db_rows:
            self.tree.insert('', 0, text= row[1], values= row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0


    def add_product(self):
        if self.validation():
            print(self.name.get())
            print(self.price.get())
        else:
            print("Name and price required")
        
if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
