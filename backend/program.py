from backend.monitor import Monitor
from backend.window import Window
from backend.database.db_create import DatabaseManagement
from interface.ctk_root import App
from backend.local_handle import LocalHandle


def start():
    #Obtener resolución de pantalla (SIN EFECTO)
    Monitor.calculate_screen_dimentions()

    #Calcular dimensiones de ventana principal (SIN EFECTO)
    Window.calculate_window_dimentions()

    #Base de datos - Genera las tablas y el registro de configuración. Crea las rutas si éstas no existen
    DatabaseManagement.create_tables()

    #Arrancar instancia customtkinter
    ctk_root = App()
    ctk_root.mainloop()

    #Finalizar conexión a base de datos
    DatabaseManagement.close_connection()