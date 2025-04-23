import socket

def encrypt(message, e, n):
    ciphertext = ''
    for letter in message:
        letter = ord(letter)
        letter = pow(letter, e, n)
        ciphertext += str(letter) + ' '
    return ciphertext

def client_program():
    host = socket.gethostname() 
    port = 1044  

    client_socket = socket.socket()  
    client_socket.connect((host, port))  

    message = 'Hello, Server!'

    while message.lower().strip() != 'bye': 
        data = client_socket.recv(1024).decode()  
        print(data)
        if data == "Enter message: ":
            message = input()
            e = int(input("Enter e: "))
            n = int(input("Enter n: "))
            message = encrypt(message, e, n)
            client_socket.send(str(message).encode())
        elif data[0:2] != "N:":
            message = input("-> ")
            client_socket.send(message.encode())
        



    client_socket.close() 


if __name__ == '__main__':
    client_program()