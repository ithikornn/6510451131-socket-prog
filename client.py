import socket
from encrypt import encrypt_message, decrypt_message
from statusCode import statusCodeToMessage
import concertHall
from datetime import datetime

def start_client(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        connected = True
        login = False
        username = ""
        hall = concertHall.ConcertHall()
        while connected:
            if not login:
                msg = input("Enter command (1) login (2) sign up (3) exit : ")
                if msg not in ["1", "2", "3"]:
                    print("Invalid command. Please try again.")
                    continue

                if msg == "1":
                    username = input("Enter username for login: ")
                    password = input("Enter password for login: ")
                    message = f"LOGIN {username} {password}"
                elif msg == "2":
                    username = input("Enter username for sign up: ")
                    password = input("Enter password for sign up: ")
                    message = f"SIGNUP {username} {password}"
                elif msg == "3":
                    message = "DISCONNECT"

                encrypted_message = encrypt_message(message)
                client.send(encrypted_message)
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") 
                print(f"[SEND] {now}")

                if msg == "3":
                    connected = False
                    print("Disconnecting from the server...")
                    continue
            else:
                hall.load_seats()
                hall.display_slots()
                msg = input("Enter your seat (e.g., A1): ")
                message = f"BOOK {msg} {username}"
                encrypted_message = encrypt_message(message)
                client.send(encrypted_message)
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") 
                print(f"[SEND] {now}")

            try:
                encrypted_response = client.recv(1024)
                response = decrypt_message(encrypted_response)  # Extract numerical status code
                response_message = statusCodeToMessage(response)
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") 
                print(f"[SERVER RESPONSE] {response} {response_message} TIME: {now}")
                if response == "200 OK":
                    login = True
                elif response in ["401 Unauthorized", "409 Conflict"]:
                    login = False
            except socket.error as e:
                print(f"Error receiving response: {e}")
    
    except socket.error as e:
        print(f"Connection error: {e}")
    
    finally:
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    start_client("127.0.0.1", 8080)
