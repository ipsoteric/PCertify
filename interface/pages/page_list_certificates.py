import customtkinter
from backend.properties import AppProperties as Props
from backend.database.db_certificates import DBCertificate
from backend.mail.email import send_emails

class PageListCertificates(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.field_width = int(int(Props.APP_WIDTH)*0.5)
        self.field_height = 100
        self.configure(height=int(Props.APP_HEIGHT))

        #Título de página
        self.title = customtkinter.CTkLabel(master=self, text=Props.TEXT_MENU_SEND_MAIL, font=("Calibri", 18))
        self.title.place(relx=0.5, rely=0.1, anchor="center")

        # Lista para almacenar los estados de los checkboxes
        self.check_vars = []

        # Crear un frame para contener los registros
        self.data_frame = customtkinter.CTkScrollableFrame(self, width=800, height=300, orientation="vertical")
        self.data_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Botón para volver a la página principal
        self.home_button = customtkinter.CTkButton(master=self, text=Props.TEXT_BACK_HOME, command=lambda: controller.show_frame("HomePage"), fg_color="red")
        self.home_button.place(relx=0.2, rely=0.8, anchor="center")

        # Botón para recargar registros
        self.load_data_button = customtkinter.CTkButton(self, text=Props.TEXT_UPDATE, command=self.reload_data)
        self.load_data_button.place(relx=0.5, rely=0.2, anchor="center")

        # Botón para eliminar registros seleccionados
        self.delete_button = customtkinter.CTkButton(self, text="Eliminar Seleccionados", command=self.delete_selection, fg_color="red")
        self.delete_button.place(relx=0.4, rely=0.8, anchor="center")

        # Botón para enviar por correo
        self.send_mail_button = customtkinter.CTkButton(self, text="Enviar Correos", command=self.starting_send_email, state="disabled")
        self.send_mail_button.place(relx=0.6, rely=0.8, anchor="center")

        #Label de confirmación (error/éxito)
        self.answer_text = customtkinter.CTkLabel(master=self, text="")
        self.answer_text.place(relx=0.5, rely=0.15, anchor="center")

        self.reload_data()



    # Recargar registros
    def reload_data(self):

        for widget in self.data_frame.winfo_children():
            widget.destroy()

        self.check_vars = []

        certificates = DBCertificate.get_certificates()

        for record in certificates:
            is_sended = "Enviado" if record[3] == 1 else "Pendiente"
            list_record = list(record)
            list_record[3] = is_sended

            var = customtkinter.StringVar(value="0")
            self.check_vars.append((var, record[0]))
            frame = customtkinter.CTkFrame(master=self.data_frame)
            frame.pack(pady=5, padx=5, fill="x")
            checkbox = customtkinter.CTkCheckBox(master=frame, text=f"{list_record[1]} ({list_record[4]}) - {list_record[2]} ({list_record[3]})", variable=var, onvalue=str(record[0]), offvalue="0")
            checkbox.pack(side="left", padx=10)

    

    def starting_send_email(self):
        items_selected = [registro_id for var, registro_id in self.check_vars if var.get() != "0"]

        if not items_selected:
            self.answer_text.configure(text="No se seleccionó ningún certificado.", text_color="red")
            return

        certificates_selected = DBCertificate.get_selected_certificates()
        
    

    def delete_selection(self):
        items_selected = [registro_id for var, registro_id in self.check_vars if var.get() != "0"]
        
        if not items_selected:
            self.answer_text.configure(text="No se seleccionó ningún certificado.", text_color="red")
            return
        
        DBCertificate.delete_certificates(items_selected)
        self.reload_data()
        self.answer_text.configure(text="Certificados eliminados correctamente.", text_color="green")