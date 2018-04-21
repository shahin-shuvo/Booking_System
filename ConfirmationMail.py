import smtplib
from email.mime import multipart,text as mailText

def send_mail(msg_body,toaddr):
    fromaddr = "lab.project.manager@gmail.com"
    # toaddr = "shahrearbinamin01@gmail.com"
    msg = multipart.MIMEMultipart()
    msg['From'] = "DU Booking"
    msg['To'] = toaddr
    msg['Subject'] = "DU Booking Request Confirmation"

    msg.attach(mailText.MIMEText(msg_body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("lab.project.manager@gmail.com", "project515557")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
