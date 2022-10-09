import socket
import time

HOST = 'localhost'
PORT = 4000

s = socket.socket()
s.bind((HOST, PORT))

print(f'Aguardando conexão na porta : {PORT}')

s.listen(5)
conn, address = s.accept()

print(f'Recebendo solicitação de {address}')

messages = [
    f'Mensagem {letter}' for letter in ['A', 'B', 'C'] 
]

for message in messages:
    message = bytes(message, 'utf-8')
    conn.send(message)
    time.sleep(4)

conn.close()