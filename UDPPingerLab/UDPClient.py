# References used
# https://docs.python.org/3/library/socket.html
# https://docs.python.org/3/howto/sockets.html

import socket
import time

# setup the client
HOST = "127.0.0.1"  # localhost
PORT = 12000  # server port
# AF_INET is IPv4
# SOCK_DGRAM is UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)

# store some data
times = []
numReqs = 10
failures = 0

print("\n----------------------------")
print(f"Sending {numReqs} pings to server")
print("----------------------------")

# send 10 pings to the server
for i in range(1, numReqs + 1):

    current_time = time.time()
    message = f"Ping {i}  {current_time}"
    message = message.encode()

    client_socket.sendto(message, (HOST, PORT))

    try:
        data, address = client_socket.recvfrom(1024)
        receive_time = time.time()
        rtt = receive_time - current_time
        times.append(rtt)
        print(f"{data.decode()} | rtt: {rtt:.5f}")

    except TimeoutError:
        print("Request timed out")
        failures += 1


# show results
minimum = min(times)
maximum = max(times)
average = sum(times) / len(times)

print("\n----------------------------")
print("Stats:")
print("----------------------------")

print(f"Maximum RTT: {maximum:.5f}")
print(f"Minimum RTT: {minimum:.5f}")
print(f"Average RTT: {average:.5f}")
print(f"Packet Loss Rate: {(failures/numReqs) * 100}%")