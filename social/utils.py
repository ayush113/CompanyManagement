from collections import namedtuple
from email import encoders as Encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


sendEmail = "ayush.work113@gmail.com"
sendPwd = "@yu$hkum@r123"

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def send_mail(subject, message, rec_name, rec_email):

    msg = MIMEMultipart()
    print("stage 1")
    msg['Subject'] = subject
    msg['From'] = ""
    msg['To'] = "%s <%s>" % (rec_name, rec_email)

    msg.attach(MIMEText(message, "html"))

    # for attach in attachs:
    #     part = MIMEBase('application', 'octet-stream')
    #     part.set_payload(open(attach, 'rb').read())
    #     Encoders.encode_base64(part)
    #     part.add_header('Content-Disposition',
    #                     'attachment; filename="%s"' % basename(attach))
    #     msg.attach(part)

    try:
        print("stage 2")
        smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_obj.ehlo()  # CONNECTS WITH HOST
        smtp_obj.starttls()  # TLS --> TRANSPORT LAYER SECURITY
        smtp_obj.ehlo()
        print("stage3")
        smtp_obj.login(sendEmail, sendPwd)
        smtp_obj.sendmail(sendEmail, rec_email, msg.as_string())
        print("success")
        smtp_obj.close()
        return True  # YAY! MAIL IS SENT!
    except smtplib.SMTPException:
        return False  # NOOO! MAIL IS NOT SENT!