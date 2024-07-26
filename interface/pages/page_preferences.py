import customtkinter
from backend.properties import AppProperties as Props
from backend.database.db_app_preferences import DBAppPreferences

class PagePreferences(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.field_width = int(int(Props.APP_WIDTH)*0.5)
        self.field_height = 100
        self.configure(height=int(Props.APP_HEIGHT))

        #Título de página
        self.title = customtkinter.CTkLabel(master=self, text=Props.TEXT_MENU_APP_SETTINGS, font=("Calibri", 18))
        self.title.place(relx=0.5, rely=0.08, anchor="center")

        #Cargar data
        self.preferences = DBAppPreferences.get_data()

        # Formulario
        self.create_form()

        # Botón para volver a la página principal
        self.home_button = customtkinter.CTkButton(master=self, text=Props.TEXT_CANCEL_PREF, command=lambda: controller.show_frame("HomePage"), fg_color="red")
        self.home_button.place(relx=0.4, rely=0.8, anchor="center")

        #Botón para enviar formulario
        self.submit_button = customtkinter.CTkButton(master=self, text=Props.TEXT_SAVE_PREF, command=self.button_update_preferences)
        self.submit_button.place(relx=0.6, rely=0.8, anchor="center")

        #Label de confirmación (error/éxito)
        self.answer_text = customtkinter.CTkLabel(master=self, text="")
        self.answer_text.place(relx=0.5, rely=0.125, anchor="center")


    def create_form(self):
        form_frame = customtkinter.CTkFrame(self)
        form_frame.place(relx=0.5, rely=0.45, anchor="center")

        # Nombre de la compañía
        company_name_label = customtkinter.CTkLabel(form_frame, text=Props.PREF_COMPANY_NAME)
        company_name_label.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.company_name_entry = customtkinter.CTkEntry(form_frame, width=self.field_width)
        self.company_name_entry.insert(0, self.preferences[1])
        self.company_name_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

        # Nombre de la compañía
        director_name_label = customtkinter.CTkLabel(form_frame, text=Props.PREF_DIRECTOR_NAME)
        director_name_label.grid(row=1, column=0, pady=5, padx=5, sticky="w")
        self.director_name_entry = customtkinter.CTkEntry(form_frame, width=self.field_width)
        self.director_name_entry.insert(0, self.preferences[2])
        self.director_name_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        # Email
        email_label = customtkinter.CTkLabel(form_frame, text=Props.PREF_EMAIL)
        email_label.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        self.email_entry = customtkinter.CTkEntry(form_frame, width=self.field_width)
        self.email_entry.insert(0, self.preferences[3])
        self.email_entry.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        # Contraseña
        password_label = customtkinter.CTkLabel(form_frame, text=Props.PREF_PASSWORD)
        password_label.grid(row=3, column=0, pady=5, padx=5, sticky="w")
        self.password_entry = customtkinter.CTkEntry(form_frame, width=self.field_width, show="*")
        self.password_entry.insert(0, self.preferences[8])
        self.password_entry.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

        # Texto de presentación
        pretext_label = customtkinter.CTkLabel(form_frame, text=Props.PREF_PRE_NAME)
        pretext_label.grid(row=4, column=0, pady=5, padx=5, sticky="w")
        self.pretext_entry = customtkinter.CTkEntry(form_frame, width=self.field_width)
        self.pretext_entry.insert(0, self.preferences[4])
        self.pretext_entry.grid(row=4, column=1, pady=5, padx=5, sticky="ew")

        # Texto de subtítulo
        post_text_label = customtkinter.CTkLabel(form_frame, text=Props.PREF_POST_NAME)
        post_text_label.grid(row=5, column=0, pady=5, padx=5, sticky="w")
        self.post_text_entry = customtkinter.CTkEntry(form_frame, width=self.field_width)
        self.post_text_entry.insert(0, self.preferences[5])
        self.post_text_entry.grid(row=5, column=1, pady=5, padx=5, sticky="ew")

        # Descripción
        description_label = customtkinter.CTkLabel(form_frame, text=Props.PREF_DESCRIPTION)
        description_label.grid(row=6, column=0, pady=5, padx=5, sticky="w")
        self.description_entry = customtkinter.CTkTextbox(form_frame, width=self.field_width, wrap="word", height=self.field_height)
        self.description_entry.insert('1.0', self.preferences[6])
        self.description_entry.grid(row=6, column=1, pady=5, padx=5, sticky="ew")

        # Porcentaje de aprobación
        per_approval_label = customtkinter.CTkLabel(form_frame, text=Props.PREF_PER_APPROVAL)
        per_approval_label.grid(row=7, column=0, pady=5, padx=5, sticky="w")
        self.per_approval_entry = customtkinter.CTkEntry(form_frame, width=self.field_width)
        self.per_approval_entry.insert(0, self.preferences[7])
        self.per_approval_entry.grid(row=7, column=1, pady=5, padx=5, sticky="ew")

    
    def button_update_preferences(self):
        description = self.description_entry.get("1.0", "end-1c")

        if self.company_name_entry.get() == "" or self.director_name_entry.get() == "" or self.email_entry.get() == "" or self.pretext_entry.get() == "" or self.post_text_entry.get() == "" or description == "" or self.per_approval_entry.get() == "":
            self.answer_text.configure(text="Hay campos que son obligatorios", text_color="red")
            return
        
        if "{organizacion}" not in description or "{porcentaje}" not in description:
            self.answer_text.configure(text="El texto debe contener {organizacion} y {porcentaje}", text_color="red")
            return
        
        #Actualizar en la base de datos
        DBAppPreferences.update(company=self.company_name_entry.get(), director=self.director_name_entry.get(), email=self.email_entry.get(), pre_name=self.pretext_entry.get(), post_name=self.post_text_entry.get(), description=self.description_entry.get("1.0", "end-1c"), per_approval=self.per_approval_entry.get(), password=self.password_entry.get())
        
        self.answer_text.configure(text="Guardado con éxito", text_color="green")