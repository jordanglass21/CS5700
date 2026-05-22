# References used
# https://docs.python.org/3/library/socket.html
# https://docs.python.org/3/howto/sockets.html
# https://datatracker.ietf.org/doc/html/rfc5321
# https://docs.python.org/3/library/base64.html
# https://docs.python.org/3/library/ssl.html
# https://support.google.com/accounts/answer/185833

from socket import *
import ssl
import base64
import os

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
HOST = "smtp.gmail.com"  # gmail server
PORT = 587  # server port
BUFFER_SZ = 4096 # we needed a larger buffer for this one
mailserver = (HOST, PORT)

# google credentials
email = os.environ.get("GMAIL_ADDRESS")
password = os.environ.get("GMAIL_PASSWORD")

# Create socket for google
# AF_INET is IPv4
# SOCK_STREAM is TCP
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

# google sends an intial greeting (220)
recv_connect = clientSocket.recv(BUFFER_SZ).decode()

# we use EHLO becuase it allows for TLS
heloCommand = 'EHLO Alice\r\n'
clientSocket.send(heloCommand.encode())
clientSocket.recv(BUFFER_SZ)

# Start TLS connection with google
tls_command = "STARTTLS\r\n"
clientSocket.send(tls_command.encode())
clientSocket.recv(BUFFER_SZ)

# we need to set up an TLS tunnel to encrypt things
context = ssl.create_default_context()
secureSocket = context.wrap_socket(clientSocket, server_hostname=HOST)

# login
auth_command = "AUTH LOGIN\r\n"
secureSocket.send(auth_command.encode())
secureSocket.recv(BUFFER_SZ)

# username - needs to be in base 64 format...
user_b64 = base64.b64encode(email.encode()).decode() + "\r\n"
secureSocket.send(user_b64.encode())
secureSocket.recv(BUFFER_SZ)

# password - needs to be in base 64 format...
pass_b64 = base64.b64encode(password.encode()).decode() + "\r\n"
secureSocket.send(pass_b64.encode())
secureSocket.recv(BUFFER_SZ)

# send SMTP commands now that we have tunnel secure
mail_from = f"MAIL FROM:<{email}>\r\n"
secureSocket.send(mail_from.encode())
secureSocket.recv(BUFFER_SZ)

rcpt_to = f"RCPT TO:<{email}>\r\n"
secureSocket.send(rcpt_to.encode())
secureSocket.recv(BUFFER_SZ)

data_command = "DATA\r\n"
secureSocket.send(data_command.encode())
secureSocket.recv(BUFFER_SZ)

# send actual message
secureSocket.send(msg.encode())

# send period indicating end of message
secureSocket.send(endmsg.encode())
secureSocket.recv(BUFFER_SZ)

quit_command = "QUIT\r\n"
secureSocket.send(quit_command.encode())
secureSocket.recv(BUFFER_SZ)

secureSocket.close()
