import smtplib

def send_email(message, toaddrs):
  fromaddr = 'campinggroundfound@gmail.com'
  username = 'campinggroundfound@gmail.com'
  password = 'Camp1ngG0'
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(username, password)
  server.sendmail(fromaddr, toaddrs, 
      'Subject: The camping ground that you want is found.\n' + message)
  server.quit()