import smtplib
import os
from email.message import EmailMessage
from email.utils import make_msgid
import imghdr

class SendMail():
    def __init__(self):
        super().__init__()

    def Send(self, patientName, patientID, reciverMail, analysis, analysisType, value):
        smtpServer = 'mail.ismaildurcan.com.tr'
        with open('mailDetail.txt', 'r') as f:
            detail = f.readlines()
        senderMail = detail[0].strip()
        password = detail[1].strip()
        port = 587
        subject = 'Patient: {} Results: {}'.format(patientName,analysisType)

        body = """Patient: {}\nPatient ID: {}\nPatient Type: {}\n\nAttention! {} was detected with a probability of %{} in the patient.""".format(patientName,patientID,analysisType,analysisType,value)

        eMail = EmailMessage()
        eMail['From'] = senderMail
        eMail['To'] = reciverMail
        eMail['Subject'] = subject
        eMail.set_content(body)


        with open(analysis, 'rb') as img:
            image_data = img.read()
            image_type = imghdr.what(img.name)
            image_name = img.name
        eMail.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

        try:
            smtp = smtplib.SMTP(smtpServer,port)
            smtp.login(senderMail, password)
            smtp.sendmail(senderMail, reciverMail, eMail.as_string())
            smtp.quit()
        except smtplib.SMTPException:
            print('error')
