import customtkinter
from backend.properties import AppProperties as Props
from PIL import Image
from backend.database.db_app_preferences import DBAppPreferences
import os
import subprocess
import tkinter.messagebox as messagebox

#PÁGINA PRINCIPAL PARA EL MENÚ DE OPCIONES
class HomePage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #Label de confirmación (error/éxito)
        self.answer_text = customtkinter.CTkLabel(master=self, text="")
        self.answer_text.place(relx=0.5, rely=0.2, anchor="center")

        #Cargar banner
        self.banner_image = Image.open(Props.APP_BANNER_PATH)
        #self.banner_photo = ImageTk.PhotoImage(self.banner_image)
        self.banner_photo = customtkinter.CTkImage(light_image=self.banner_image, size=(900,100))


        #CTKLabel para banner
        self.banner_label = customtkinter.CTkLabel(master=self, image=self.banner_photo, text="")
        self.banner_label.grid(row=0, column=0, columnspan=controller.total_columns, sticky="ew")

        #CTKFrame para el body
        self.body_frame = customtkinter.CTkFrame(master=self, width=int(Props.APP_WIDTH), height=int(int(Props.APP_HEIGHT)-50))
        self.body_frame.grid(column=0, row=1, columnspan=controller.total_columns)

        #Título principal
        self.title_menu = customtkinter.CTkLabel(master=self.body_frame, text=Props.TITLE_MENU_OPTIONS, font=("Calibri", 18))
        self.title_menu.place(relx=0.5, rely=0.1, anchor="center")

        #Menú principal
        self.option1 = customtkinter.CTkButton(self.body_frame, text=Props.TEXT_MENU_CREATE_CERTIFICATE, command=lambda: controller.show_frame("Page1"), width=Props.WIDTH_MENU_OPTIONS)
        self.option1.place(relx=0.5, rely=0.2, anchor="center")

        # self.option2 = customtkinter.CTkButton(self.body_frame, text=Props.TEXT_MENU_CREATE_CERTIFICATES, command=self.button_callback, width=Props.WIDTH_MENU_OPTIONS)
        # self.option2.place(relx=0.5, rely=0.3, anchor="center")

        self.option3 = customtkinter.CTkButton(self.body_frame, text=Props.TEXT_MENU_SEND_MAIL, command=lambda: controller.show_frame("PageListCertificates"), width=Props.WIDTH_MENU_OPTIONS)
        self.option3.place(relx=0.5, rely=0.3, anchor="center")

        self.option4 = customtkinter.CTkButton(self.body_frame, text=Props.TEXT_MENU_CREATE_COURSE, command=lambda: controller.show_frame("PageCourse"), width=Props.WIDTH_MENU_OPTIONS)
        self.option4.place(relx=0.5, rely=0.4, anchor="center")

        self.option5 = customtkinter.CTkButton(self.body_frame, text=Props.TEXT_MENU_APP_SETTINGS, command=lambda: controller.show_frame("PagePreferences"), width=Props.WIDTH_MENU_OPTIONS)
        self.option5.place(relx=0.5, rely=0.5, anchor="center")

        self.option6 = customtkinter.CTkButton(self.body_frame, text="Abrir directorio de archivos", command=self.open_file, width=Props.WIDTH_MENU_OPTIONS, fg_color="green")
        self.option6.place(relx=0.5, rely=0.6, anchor="center")

        self.option7 = customtkinter.CTkButton(self.body_frame, text="Salir", command=controller.destroy, width=Props.WIDTH_MENU_OPTIONS, fg_color="red")
        self.option7.place(relx=0.5, rely=0.7, anchor="center")

    def button_callback(self):
        print("button pressed")

    def open_file(self):
        folder_path = DBAppPreferences.get_specific_data(9)

        if os.path.exists(folder_path):
            try:
                subprocess.Popen(f'explorer "{folder_path}"')
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", f"La ruta {folder_path} no existe.")