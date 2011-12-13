import smtplib, getpass

fromaddr = raw_input('Who is this being sent from? ')
toaddrs  = raw input('Who are you sending it to? ')
msg = raw_input('What is the message you are sending? ')
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
# Credentials (if needed)
username = raw_input('Username: ')
password = getpass.getpass('Password: ')
server.login(username,password)
del password
# The actual mail send
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
