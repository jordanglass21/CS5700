# References used
# https://docs.python.org/3/library/socket.html
# https://docs.python.org/3/howto/sockets.html
# https://datatracker.ietf.org/doc/html/rfc5321
# https://mailpit.axllent.org/

from socket import *
msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
HOST = "127.0.0.1"  # localhost
PORT = 1025  # server port
BUFFER_SZ = 1024
mailserver = (HOST, PORT)

# Create socket called clientSocket and establish a TCP connection with mailserver
# AF_INET is IPv4
# SOCK_STREAM is TCP
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

# display
print("\n---------------")
print("Local Mail Client")
print("---------------\n")


recv = clientSocket.recv(BUFFER_SZ).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(BUFFER_SZ).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
mail_from = "MAIL FROM: <alice@network.com>\r\n"
clientSocket.send(mail_from.encode())
recv2 = clientSocket.recv(BUFFER_SZ).decode()
print(recv2)

# Send RCPT TO command and print server response.
rcpt_to = "RCPT TO: <bob@network.com>\r\n"
clientSocket.send(rcpt_to.encode())
recv3 = clientSocket.recv(BUFFER_SZ).decode()
print(recv3)

# Send DATA command and print server response.
data_command = "DATA\r\n"
clientSocket.send(data_command.encode())
recv4 = clientSocket.recv(BUFFER_SZ).decode()
print(recv4)

# Send message data.
clientSocket.send(msg.encode())

# Message ends with a single period.
clientSocket.send(endmsg.encode())
recv5 = clientSocket.recv(BUFFER_SZ).decode()
print(recv5)

# Send QUIT command and get server response.
quit_command = "QUIT\r\n"
clientSocket.send(quit_command.encode())
recv6 = clientSocket.recv(BUFFER_SZ).decode()
print(recv6)

clientSocket.close()
