import socket
from Crypto.Cipher import AES

def rsa_encrypt(message, e, n):
    result = ''
    for char in message:
        result += str(pow(ord(char), e, n)) + ' '
    return result.strip()

def client_program():
    host = socket.gethostname()
    port = 1044

    client_socket = socket.socket()
    client_socket.connect((host, port))

    key = b'Sixteen byte key'

    while True:
        data = client_socket.recv(1024).decode()
        print(data)

        if data.startswith("Enter k-bits:"):
            k_bits = input("-> ")
            client_socket.send(k_bits.encode())

            pubkey = client_socket.recv(1024).decode()
            print("Received public key:", pubkey)
            n, e = map(int, pubkey.split(','))

        elif data.startswith("Enter message:"):
            message = input()
            rsa_encrypted = rsa_encrypt(message, e, n)
            print("RSA Encrypted message:", rsa_encrypted)

            cipher = AES.new(key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(rsa_encrypted.encode())
            print("AES Encrypted message:", ciphertext)
            
            client_socket.send(ciphertext)
            client_socket.send(tag)
            client_socket.send(cipher.nonce)

            continue

    client_socket.close()

if __name__ == '__main__':
    client_program()