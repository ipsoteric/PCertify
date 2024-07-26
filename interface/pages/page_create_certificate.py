import customtkinter
from backend.database.db_certificates import DBCertificate
from backend.database.db_courses import  DBCourse
from backend.properties import AppProperties as Props
from backend.certificate import generate_certificate
from utilities.utilities import get_date, fullname_format
from backend.aws_upload import upload_file
from backend.qr_codes import generate_qr_code
import os

#PÁGINA PARA GENERAR CERTIFICADOS INDIVIDUALES
class Page1(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(height=int(Props.APP_HEIGHT))

        self.title = customtkinter.CTkLabel(master=self, text=Props.TEXT_MENU_CREATE_CERTIFICATE, font=("Calibri", 18))
        self.title.place(relx=0.5, rely=0.1, anchor="center")

        # Formulario
        self.create_form()

        # Botón para volver a la página principal
        self.home_button = customtkinter.CTkButton(master=self, text=Props.TEXT_BACK_HOME, command=lambda: controller.show_frame("HomePage"), fg_color="red")
        self.home_button.place(relx=0.2, rely=0.8, anchor="center")

        #Botón para enviar formulario
        self.submit_button = customtkinter.CTkButton(master=self, text=Props.TEXT_SUBMIT_USER, command=self.submit_form)
        self.submit_button.place(relx=0.4, rely=0.8, anchor="center")

        #Label de confirmación (error/éxito)
        self.answer_text = customtkinter.CTkLabel(master=self, text="")
        self.answer_text.place(relx=0.5, rely=0.2, anchor="center")


    def create_form(self):
        form_frame = customtkinter.CTkFrame(self)
        form_frame.place(relx=0.5, rely=0.4, anchor="center")

        # Nombre
        name_label = customtkinter.CTkLabel(form_frame, text="Nombre completo:")
        name_label.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.name_entry = customtkinter.CTkEntry(form_frame, width=int(int(Props.APP_WIDTH)*0.5))
        self.name_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

        # Email
        email_label = customtkinter.CTkLabel(form_frame, text="Email:")
        email_label.grid(row=1, column=0, pady=5, padx=5, sticky="w")
        self.email_entry = customtkinter.CTkEntry(form_frame, width=int(int(Props.APP_WIDTH)*0.5))
        self.email_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        # Lista desplegable
        courses = DBCourse.get_data_name()
        courses.insert(0, Props.TEXT_SELECT_COURSE)
        courses_label = customtkinter.CTkLabel(form_frame, text="Curso:")
        courses_label.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        self.course_options_menu = customtkinter.CTkOptionMenu(form_frame, values=courses, width=int(int(Props.APP_WIDTH)*0.5))
        self.course_options_menu.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        # Checkbox para abrir archivo pdf generado
        self.pdf_var = customtkinter.StringVar(value="0")
        self.checkbox_pdf = customtkinter.CTkCheckBox(master=form_frame, text="Abrir documento PDF", variable=self.pdf_var)
        self.checkbox_pdf.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

        # Checkbox para abrir archivo QR generado
        self.qr_var = customtkinter.StringVar(value="0")
        self.checkbox_qr = customtkinter.CTkCheckBox(master=form_frame, text="Abrir QR", variable=self.qr_var)
        self.checkbox_qr.grid(row=4, column=1, pady=5, padx=5, sticky="ew")


    def submit_form(self):
        fullname = self.name_entry.get()
        email = self.email_entry.get()
        course_option = self.course_options_menu.get()

        if not fullname or course_option==Props.TEXT_SELECT_COURSE:
            self.answer_text.configure(text="Todos los campos son obligatorios", text_color="red")
            return
        
        fullname_cleanned = fullname_format(fullname)
        email_cleanned = email.lower()
        
        #Obtener la fecha actual
        date = get_date()

        #Generar fichero de certificado
        certificate_info = generate_certificate(fullname_cleanned, course_option, date)
        filename = certificate_info["filename"] #Nombre archivo
        file_output_path = certificate_info["pdf_output_path"] #Ruta de salida de archivo
        qr_file_path = certificate_info["qr_file_path"] #Ruta de salida de QR

        ##Subir a Bucket S3 de AWS
        s3_file_url = upload_file(file_path=file_output_path, bucket_name=Props.BUCKET_NAME, object_name=filename)

        #Generar código QR
        generate_qr_code(data=s3_file_url, file_path=qr_file_path)
        
        #Guardar en la base de datos
        DBCertificate.save_certificate(fullname=fullname_cleanned, email=email_cleanned, course=course_option, date=date)
        self.answer_text.configure(text="Se ha creado el certificado", text_color="green")

        #Abrir PDF
        if not self.pdf_var.get() == "0":
            os.startfile(file_output_path)

        #Abrir QR
        if not self.qr_var.get() == "0":
            os.startfile(qr_file_path)


        #Limpiar campos
        self.name_entry.delete(0,"end")
        self.email_entry.delete(0,"end")