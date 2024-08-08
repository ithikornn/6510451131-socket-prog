import socket
import json
import os
from encrypt import encrypt_message, decrypt_message
from concertHall import ConcertHall
from datetime import datetime

# Path to the JSON file
file_path = 'users.json'

login_user = []

def load_users():
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return []

def save_users(users):
    with open(file_path, 'w') as file:
        json.dump(users, file, indent=4)

def handle_client(conn):
    users = load_users()
    hall = ConcertHall()
    username = ""
    while True:
        encrypted_data = conn.recv(1024)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") 
        if not encrypted_data:
            break
        
        try:
            data = decrypt_message(encrypted_data)
            command = data.split()
            print(f"[RECIVED] {now}")
            
            if command[0] == "LOGIN":
                username, password = command[1], command[2]
                user_found = any(user['username'] == username and user['password'] == password for user in users)
                if user_found:
                    response = "200"
                    hall.display_slots()
                    login_user.append(username)
                else:
                    response = "401"
            
            elif command[0] == "SIGNUP":
                username, password = command[1], command[2]
                if any(user['username'] == username for user in users):
                    response = "409"
                else:
                    users.append({'username': username, 'password': password})
                    save_users(users)
                    response = "201"
            
            elif command[0] == "DISCONNECT":
                if username in login_user:
                    login_user.remove(username)
                response = "204"
                conn.send(encrypt_message(response))
                break

            elif command[0] == "BOOK":
                if username not in login_user:
                    response = "401 Unauthorized"  # Correct response code for not logged in
                else:
                    seats = command[1]
                    row = seats[0]
                    col = int(seats[1])
                    response = hall.book_seat(row, col, username)
                    hall.display_slots() 

            else:
                response = "400"
            
            print(f"[SERVER RESPONSE] {response}")
            conn.send(encrypt_message(response))
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") 
            print(f"[SEND] {now}")

        except Exception as e:
            print(f"Error handling client data: {e}")
            conn.send(encrypt_message("500 Internal Server Error"))
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") 
            print(f"[SEND] {now}")
    
    conn.close()

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr}")
        handle_client(conn)

if __name__ == "__main__":
    start_server("0.0.0.0", 8080)
