from backend.database.db_app_preferences import DBAppPreferences
from email.message import EmailMessage
import ssl
import smtplib


#email_sender = "sender@example.com"
#password = ""
#email_reciver = "reciver@example.com"
#
#subject = "Asunto"
#body = "Contenido del mensaje"
#
#em = EmailMessage()
#em["From"] = email_sender
#em["To"] = email_reciver
#em["Subject"] = subject
#em.set_content(body)
#
#context = ssl.create_default_context()
#
#with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as smtp:
#    smtp.login(email_sender, password)
#    smtp.sendmail(email_sender, email_reciver, em.as_string())



def send_emails(checkboxes):
    selected_emails = [email for checkbox, var, email in checkboxes if var.get() == 1]

    if selected_emails:
        for email in selected_emails:
            send_email(email)


def send_email(certificate_info):
    preferences = DBAppPreferences.get_data()
    #print(f"correo enviado a {to_email}")
    from_email = preferences[2]
    #from_password = "tucontraseña"
#
    #subject = "Certificado de Aprobación"
    #body = "Estimado(a),\n\nAdjunto a este correo encontrará su certificado de aprobación del curso.\n\nSaludos."
#
    #msg = MIMEMultipart()
    #msg['From'] = from_email
    #msg['To'] = to_email
    #msg['Subject'] = subject
#
    #msg.attach(MIMEText(body, 'plain'))
#
    #try:
    #    server = smtplib.SMTP('smtp.dominio.com', 587)
    #    server.starttls()
    #    server.login(from_email, from_password)
    #    text = msg.as_string()
    #    server.sendmail(from_email, to_email, text)
    #    server.quit()
    #    print(f"Correo enviado a {to_email}")
    #except Exception as e:
    #    print(f"Error al enviar correo a {to_email}: {e}")
    