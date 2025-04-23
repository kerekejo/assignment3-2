import socket
import random

def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generatekbits(k):
    while True:
        num = random.getrandbits(k)
        num |= 1
        if is_prime(num):
            return num
        
def decrypt(ciphertext, d, n):
    plaintext = ''
    ciphertext = ciphertext.split()
    for letter in ciphertext:
        letter = int(letter)
        letter = pow(letter, d, n)
        plaintext += chr(letter)
    return plaintext

def server_program():
    
    host = socket.gethostname()
    port = 1044

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port)) 

    server_socket.listen(2)
    conn, address = server_socket.accept()  
    print("Connection from: " + str(address))
    #data = "Hello, Client!"
    #conn.send(data.encode()) 

    while True:
        message = "Enter k-bits: "
        conn.send(message.encode())
        data = conn.recv(1024).decode()
        try:
            k = int(data)
            if k <= 0:
                break
            else:
                p = generatekbits(k)
                q = generatekbits(k)
                n = p * q
                phi = (p - 1) * (q - 1)
                e = 17
                d = pow(e, -1, phi)
                conn.send(f"N: {n}, e: {e}".encode())
                conn.send("Enter message: ".encode())
                encryptedMessage = conn.recv(1024).decode()
                print(f"Received message: {encryptedMessage}")
                print(decrypt(encryptedMessage, d, n))

                
                
        except ValueError:
            break
        
        
        
        
        if not data:
            break
        
         


    conn.close() 
server_program()