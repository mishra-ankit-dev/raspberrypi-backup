
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
 
fromaddr = "amishm766@gmail.com"
toaddr = "am9713490290@gmail.com"
 
msg = MIMEMultipart()
 
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "image"
 
body = "he has entered wrong password"
 
msg.attach(MIMEText(body, 'plain'))
 
filename = "/var/www/html/image.jpg"
attachment = open(filename, "rb")
 
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
msg.attach(part)
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "amishm766@")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
print("sent email to %s" % toaddr)
