import socket
import threading
import tkinter as tk
from turtle import update
window = tk.Tk()
window.title("Sever")

# Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Connect", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Host: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="*******************CLIENT LIST*****************").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=15, width=40)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
# Insert demo connected user names
tkDisplay.insert(tk.END, "User 1\n")
tkDisplay.insert(tk.END, "User 2\n")
tkDisplay.insert(tk.END, "User 3\n")
tkDisplay.insert(tk.END, "User 4\n")
tkDisplay.insert(tk.END, "User 5\n")
tkDisplay.insert(tk.END, "User 6\n")
tkDisplay.insert(tk.END, "User 7\n")
tkDisplay.insert(tk.END, "User 8\n")
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

def start_server():
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)


def stop_server():
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)


server = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080
client_name = ""
clients = []
clients_name = []
 
 # Starting the server function

def start_server():

    btnStart.config(state=tk.DISABLED)
    btnStop.config(start=tk.NORMAL)

    global server,HOST_ADDR,HOST_PORT
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"]= "HOST:", HOST_ADDR
    lblPort["text"]= "PORT:", HOST_PORT


def accept_clients(the_server, y):
    while True:
        client, addr = the_server.accept()
        clients.append(client)

        threading._start_new_thread(send_receive_client_message, (client,addr))


def send_receive_client_message(client_conn, client_addr):
    global server,clients_name, clients, clients_addr
    client_msg = " "

    # sent welcome msg to the client

    client_name = client_conn(4096)
    client_conn.send("Welcome", client_name, "Use 'exit' to quit")

    clients_name.append(client_name)

    update_client_names_display(clients_name)

    while True:
        data = client_conn.recv(4096)
        if not data:break
        if data == "exit":break

        client_msg = data

        idx = get_client_index(clients, client_conn)
        sending_client_name = client_name[idx]

        for c in clients:
            if c != client_conn:
                c.send(sending_client_name,"->", client_msg)

        
    idx = get_client_index(clients, client_conn)
    del clients_name[idx]
    del clients[idx]
    client_conn.close()


    update_client_names_display(clients_name)


def get_client_index(client_list, curr_client):
    idx = 0

    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


def update_client_names_display(name_list):
    tkDisplay.config(state = tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)


    for c in name_list:
        tkDisplay.insert(tk.END, c, "\n")

    tkDisplay.config(state=tk.DISABLED)

window.mainloop()