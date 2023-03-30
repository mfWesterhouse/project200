import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '192.168.1.243'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames = []
questions = [
    "What is good morning? \n a. Bonsoir \n b. Au revoir \n c. Bonjour",
    "What is hi or bye? \n a. Salut \n b. Enchante \n c. Lait",
    "What is cat? \n a. Chat \n b. Gato \n c. Garcon",
    "What is dog? \n a. Noir \n b. Chien \n c. Femme",
    "What is husband? \n a. Marie \n b. Pere \n c. Mari"
]
answers = [
    "c", "a", "a", "b", "c"
]

print("Server has started...")

def get_random_question_answer(conn):
    random_index = random.randit(0, len(questions) -1)
    random_question = questions(random_index)
    random_answer = answers(random_index)
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn, nickname):
    conn.send("Welcome to this chatroom!".encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                print(message)
                broadcast(message, conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname): 
    if nickname in nicknames: 
        nicknames.remove(nickname)

while True:
    conn, addr = server.accept()
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    message = "{} joined!".format(nickname)
    print(message)
    broadcast(message, conn)
    new_thread = Thread(target = clientthread,args = (conn.nickname))
    new_thread.start()