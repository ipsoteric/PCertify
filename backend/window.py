from .monitor import Monitor

#Clase para calcular las dimensiones de la ventana de la aplicación
class Window():
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
    def calculate_window_dimentions(cls):
        Monitor.calculate_screen_dimentions()
        screen_width = Monitor.get_width()
        screen_height = Monitor.get_height()

        if(screen_width >= 1920):
            cls.set_width(900)
            cls.set_height(600)
        
        else:
            cls.set_width(600)
            cls.set_height(400)