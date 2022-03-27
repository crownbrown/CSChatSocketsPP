# Name: Steve Thatcher
# OSU Email: thatches@oregonstate.edu
# Course: CS372 - Intro to Computer Networks
# Assignment: Programming Project: Client-Server Chat
# Due Date: 03/13/22
# Description: Using the Python Socket API this program creates a SERVER
#     which can accept connections from 1 client for a text-based chat.
#     Adapted from sample code in Kurose and Ross, Computer Networking:
#     A Top-Down Approach, 7th Edition, Pearson section 2.7.


from socket import *


def server_send_message(currSocket):
    print("\r")
    user_message = str(input("Type /q to quit\nEnter message to send: \n>"))
    while user_message == "":  # checks for empty message, prompts again
        user_message = input("Type /q to quit\nEnter message to send: ")
    # calculates message length, as well as length of length, combines into one
    user_message_length = len(user_message)
    length_of_length = len(str(user_message_length))
    total_message_length = user_message_length + 2 + length_of_length
    complete_message_with_len = str(total_message_length) + "\n" + user_message
    currSocket.send(complete_message_with_len.encode())  # encodes to bin, send
    if user_message == "/q":  # if user typed /q it closes the connection
        currSocket.close()  # closes the socket connection on server side
        return
    return currSocket


def server_receive_message(currSocket):
    raw_data = currSocket.recv(256)  # requests next pkt up to 256 from client
    decoded_data = raw_data.decode()
    # splits messages into list with integer for message length, and string
    split_data = decoded_data.split("\n", 1)
    total_length = int(split_data[0])
    message_data = split_data[1]
    while total_length > 0:  # runs while there is remaining message length
        print(message_data, end="")  # continues printing on same line
        total_length -= 256
        if message_data == "/q":  # if client send /q it closes the connection
            currSocket.close()  # closes the socket connection on server side
            return
        if total_length > 0:
            raw_data = currSocket.recv(256)  # requests next pkt up to 256
            message_data = raw_data.decode()
    return currSocket


def open_socket():
    serverHost = '127.0.0.1'  # URI or IP address for socket
    serverPort = 12023  # port addresses for socket
    serverSocket = socket(AF_INET,SOCK_STREAM)  # Creates socket using IPv4
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # from assign desc
    serverSocket.bind((serverHost,serverPort))  # passes and binds
    serverSocket.listen(1)  # will queue up to one connection at a time
    print('Server is listening on: ',serverHost,":",serverPort)
    connectionSocket, addr = serverSocket.accept()  # new socket for client
    print('Connected by: ', addr)

    # main loop that continues as long as there is a connection
    while connectionSocket:
        connectionSocket = server_receive_message(connectionSocket)
        if not connectionSocket: # if client closes connection, ends
            return
        connectionSocket = server_send_message(connectionSocket)


open_socket()
