import socket
import random
from Crypto.Cipher import AES

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

def rsa_decrypt(ciphertext, d, n):
    decrypted = ''
    numbers = ciphertext.strip().split()
    for num in numbers:
        decrypted += chr(pow(int(num), d, n))
    return decrypted

def server_program():
    host = socket.gethostname()
    port = 1044

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from:", address)

    while True:
        conn.send(b"Enter k-bits: ")
        data = conn.recv(1024).decode()
        if not data:
            break

        try:
            k = int(data)
            if k <= 0:
                break
        except ValueError:
            break

        p = generatekbits(k)
        q = generatekbits(k)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 17
        d = pow(e, -1, phi)

        conn.send(f"{n},{e}".encode()) 

        conn.send(b"Enter message: ")
        encrypted_data = conn.recv(2048)
        tag = conn.recv(16)
        nonce = conn.recv(16)

        print("Received encrypted data:", encrypted_data)
        print("Received tag:", tag)
        print("Received nonce:", nonce)

        key = b'Sixteen byte key'
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(encrypted_data, tag)

        rsa_decrypted = rsa_decrypt(decrypted.decode(), d, n)
        print("Decrypted message:", rsa_decrypted)

    conn.close()

server_program()