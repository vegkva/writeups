import socket
import json
from time import sleep

items = ["@flesh", "@pulsating flesh", "@lit censer", "@censer", "@spiked sphere", "@bloodied altar", "@speaking wall", "@pulsating slab", "@foul phial", "@bloodied paper", "@ghoul blood", "@melted altar", "@empty phial", "@salted sword", "@dull sword", "@bubbling phial", "@sharpened sword", "@coiled rod", "@sunken altar", "@paper", "@torch", "@sword", "@armor", "@phial", "@ancient ghoul", "@banner", "@bright spark", "@marked slab", "@hieroglyphic wall", "@steel slates", "@oozing liquid", "@altar", "@moving stones", "@slit visor"]
rooms = ["central_platform", "central_hall", "stair_room", "stair_path", "pool_room", "eye_room", "dungeon_prison", "ghoul_room", "bright_room", "altar_room", "sharpening_room"]

  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("legend-of-vexillum.ctf.cybertalent.no", 2000))

result_list = []
  
def recv_until(sock, marker=b"\n"):
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            raise ConnectionAbortedError()
        data += chunk
    return data

# For manually testing
def user_input():
    while True:
        cmd = input("Enter command: ")
        if cmd == "exit":
            break
        room, items, command = cmd.split(";")
        msg = f"ROOM:{room};ITEMS:{items};COMMAND:{command};\n"
        s.send(msg.encode())
        data = recv_until(s)
        print(data.decode())

        if "with what?" in data.decode():
            cmd = input("> ")
            msg = f"{cmd}\n"
            s.send(msg.encode())
            data = recv_until(s)
            print(data.decode())
  


# Brute force combining items, and see if any new items appear
def main():
    for item in items:
        for newitem in items:
            msg1 = f"ROOM:central_hall;ITEMS:{item}{newitem};COMMAND:use {newitem.replace('@', '')};\n"
            s.send(msg1.encode())
            try:
                data = recv_until(s)
            except ConnectionAbortedError as e:
                print("Error in use, msg: ", msg1)
                print("error: ", e)
            #print(f"[*] Received data: {data.decode()}")
            if "with what?" in data.decode():
                #print(f"In room '{room}' and trying to use {item.replace('@', '').replace('_', ' ')} with {newitem}")
                msg2 = f"{item.replace('@','').replace('_', ' ')}\n"
                s.send(msg2.encode())
                try:
                    data = recv_until(s)
                except ConnectionAbortedError as e:
                    print(f"Error in with what. MSG1: {msg1}\nMSG2:{msg2}")
                    print("error: ", e)
  

                if "error:" in data.decode().lower() or data.decode().strip() == "":
                    continue
                else:
                    if data.decode() in result_list:
                        continue
                    print("#######################")
                    print(f"[+] Used item '{newitem}' with '{item}' in room 'central_hall' successfully!")
                    print(data.decode())
                    result_list.append(data.decode())
                    
                    # Check room after items has been used
                    msg = f"ROOM:central_hall;ITEMS:;COMMAND:look room;\n"
                    s.send(msg.encode())
                    data = recv_until(s)
                    print(f"[+] central_hall description after using items:\n{data.decode()}")

					          # Check item after it has been used
                    msg = f"ROOM:central_hall;ITEMS:{item}{newitem};COMMAND:look {item.replace('@', '')};\n"
                    s.send(msg.encode())
                    data = recv_until(s)
                    print(f"[+] Looking at item '{item}':\n{data.decode()}")
					
					          # Check item after it has been used
                    msg = f"ROOM:central_hall;ITEMS:{item}{newitem};COMMAND:look {newitem.replace('@', '')};\n"
                    s.send(msg.encode())
                    data = recv_until(s)
                    print(f"[+] Looking at item '{newitem}':\n{data.decode()}")

                    print("#######################\n")
