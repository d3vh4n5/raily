from email.message import EmailMessage
import ssl
import smtplib
from mailer.errors.MailSendingError import MailSendingError

'''
=========================
IMPORTANTE:
para hacer lo mismo con gmail se piden
otros permisos desde gmail desde la web.

este funciona así nada mas con hotmail
=========================
'''

'''Hacer pestaña de instrucciones en la barra de menú'''

def send_auto_mail(sender, ePass, reciever, subject, body):

    email_emisor = sender
    email_pass= ePass
    email_receptor = reciever
    asunto= subject
    cuerpo=body

    em = EmailMessage()
    em['From'] = email_emisor
    em['To'] = email_receptor
    em['Subject'] = asunto

    em.set_content(cuerpo)

    # contexto = ssl.create_default_context()

    try:

        #with smtplib.SMTP_SSL('smtp-mail.outlook.com', 587) as smtp:
        #    smtp.login(email_emisor, email_pass)
        #   smtp.sendmail(email_emisor, email_receptor, em.as_string())
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(email_emisor, email_pass)
        server.sendmail(email_emisor, email_receptor, em.as_string())
        print('Hecho!', 'Tu mensaje ha sido enviado con éxito')
        server.quit()
    except Exception as e:
        raise MailSendingError("Error al enviar el correo electrónico: {}".format(str(e)))
