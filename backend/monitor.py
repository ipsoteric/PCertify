import tkinter as tk

#Clase estática para obtener la resolución de pantalla del usuario
class Monitor():

    #Atributos para trabajar
    width : int = None
    height : int = None


    @classmethod
    def set_width(cls, new_width:int):
        cls.width = new_width

    @classmethod
    def set_height(cls, new_height:int):
        cls.height = new_height


    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_height(cls):
        return cls.height


    @classmethod
    def calculate_screen_dimentions(cls):
        #Obtener resolución de pantalla principal
        root : object = tk.Tk()
        width : int = root.winfo_screenwidth()
        height : int = root.winfo_screenheight()

        #Establecer valores
        cls.set_width(width)
        cls.set_height(height)

        #Destruir instancia tk
        root.destroy()