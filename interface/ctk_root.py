import customtkinter
from .pages.home import HomePage
from .pages.page_create_certificate import Page1
from .pages.page_preferences import PagePreferences
from .pages.page_list_certificates import PageListCertificates
from.pages.page_course import PageCourse
from backend.properties import AppProperties as Props
from backend.monitor import Monitor

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.total_columns = 4
        self.total_rows = 2
        #self.grid_columnconfigure(list(range(self.total_columns)), weight=1)
        #self.grid_rowconfigure(list(range(self.total_rows)), weight=1)

        # Obtener el tamaño de la ventana
        window_width = int(Props.APP_WIDTH)
        window_height = int(Props.APP_HEIGHT)

        # Obtener la resolución de la pantalla
        screen_width = Monitor.width
        screen_height = Monitor.height

        # Calcular la posición centrada
        position_right = int(screen_width/2 - window_width/2)
        position_down = int(screen_height/2 - window_height/2)

        self.title(Props.APP_NAME)
        self.iconbitmap(Props.APP_ICON_PATH)
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
        self.resizable(Props.APP_RESIZABLE_WIDTH, Props.APP_RESIZABLE_HEIGHT)

        # Contenedor para las páginas
        self.container = customtkinter.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, Page1, PageListCertificates, PageCourse, PagePreferences):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")


    def show_frame(self, page_name):
        if page_name in self.frames:
            self.frames[page_name].destroy()

        frame = globals()[page_name](parent=self.container, controller=self)
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

        #frame = self.frames[page_name]
        #frame.tkraise()