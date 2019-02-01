import smtplib
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("amishm766@gmail.com", "amishm766@")
 
#msg = "message from pi"
msg = open('/var/www/html/image.jpg',"rb")
server.sendmail("amishm766@gmail.com", "am9713490290@gmail.com", msg)
server.quit()