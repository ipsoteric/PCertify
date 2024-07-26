import customtkinter
from backend.database.db_certificates import DBCertificate
from backend.database.db_courses import  DBCourse
from backend.properties import AppProperties as Props

#PÁGINA PARA GENERAR CERTIFICADOS INDIVIDUALES
class PageCourse(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(height=int(Props.APP_HEIGHT))

        self.title = customtkinter.CTkLabel(master=self, text=Props.TEXT_MENU_CREATE_COURSE, font=("Calibri", 18))
        self.title.place(relx=0.5, rely=0.1, anchor="center")

        # Formulario
        self.create_form()

        #Botón para crear curso
        self.submit_button = customtkinter.CTkButton(master=self, text=Props.TEXT_CREATE_COURSE, command=self.submit_form)
        self.submit_button.place(relx=0.8, rely=0.2, anchor="center")

        #Label de confirmación (error/éxito)
        self.answer_text = customtkinter.CTkLabel(master=self, text="")
        self.answer_text.place(relx=0.5, rely=0.15, anchor="center")


        # Lista para almacenar los estados de los checkboxes
        self.check_vars = []

        # Crear un frame para contener los registros
        self.data_frame = customtkinter.CTkScrollableFrame(self, width=800, height=200, orientation="vertical")
        self.data_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Botón para volver a la página principal
        self.home_button = customtkinter.CTkButton(master=self, text=Props.TEXT_BACK_HOME, command=lambda: controller.show_frame("HomePage"), fg_color="red")
        self.home_button.place(relx=0.2, rely=0.8, anchor="center")

        # Botón para recargar registros
        self.load_data_button = customtkinter.CTkButton(self, text=Props.TEXT_UPDATE, command=self.reload_data)
        self.load_data_button.place(relx=0.6, rely=0.8, anchor="center")

        # Botón para eliminar registros
        self.delete_button = customtkinter.CTkButton(self, text=Props.TEXT_DELETE, command=self.delete_data, fg_color="red")
        self.delete_button.place(relx=0.4, rely=0.8, anchor="center")

        self.reload_data()


    def create_form(self):
        form_frame = customtkinter.CTkFrame(self)
        form_frame.place(relx=0.4, rely=0.2, anchor="center")

        # Nombre
        name_label = customtkinter.CTkLabel(form_frame, text="Nombre:")
        name_label.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.name_entry = customtkinter.CTkEntry(form_frame, width=int(int(Props.APP_WIDTH)*0.5))
        self.name_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")


    def submit_form(self):
        name = self.name_entry.get()

        if not name:
            self.answer_text.configure(text="Todos los campos son obligatorios", text_color="red")
            return
        
        #Guardar en la base de datos
        DBCourse.save(name=name)
        self.answer_text.configure(text="Curso ingresado con éxito", text_color="green")

        #Limpiar campos
        self.name_entry.delete(0,"end")

    
    # Recargar registros
    def reload_data(self):

        for widget in self.data_frame.winfo_children():
            widget.destroy()

        self.check_vars = []

        courses = DBCourse.get_data()

        for record in courses:

            var = customtkinter.StringVar(value="0")
            self.check_vars.append((var, record[0]))
            frame = customtkinter.CTkFrame(master=self.data_frame)
            frame.pack(pady=5, padx=5, fill="x")
            checkbox = customtkinter.CTkCheckBox(master=frame, text=f"{record[1]}", variable=var, onvalue=str(record[0]), offvalue="0")
            checkbox.pack(side="left", padx=10)


    # Eliminar registros
    def delete_data(self):
        items_selected = [registro_id for var, registro_id in self.check_vars if var.get() != "0"]
        
        if not items_selected:
            self.answer_text.configure(text="No se seleccionó ningún curso.", text_color="red")
            return
        
        DBCourse.delete_courses(items_selected)
        self.reload_data()
        self.answer_text.configure(text="Cursos eliminados correctamente.", text_color="green")