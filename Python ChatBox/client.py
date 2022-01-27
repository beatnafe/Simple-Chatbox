import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 2022


class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        msg = tkinter.Tk()
        msg.withdraw()
        self.username = simpledialog.askstring(
            'Username', "Please choose a username", parent=msg)
        self.done = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui)
        recevice_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        recevice_thread.start()

    def gui(self):
        self.window = tkinter.Tk()
        self.window.title(f"Logged in as: {self.username}")
        self.window.configure(bg='lightgray')
        self.chat_label = tkinter.Label(
            self.window, text="Chat: ", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=10, pady=5)
        self.text_area = tkinter.scrolledtext.ScrolledText(self.window)
        self.text_area.pack(padx=10, pady=5)
        self.text_area.config(state='disabled')
        self.msg_label = tkinter.Label(
            self.window, text="Send Message Here: ", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=10, pady=5)
        self.input_area = tkinter.Text(self.window, height=3)
        self.input_area.pack(padx=10, pady=5)
        self.send_button = tkinter.Button(
            self.window, text='Send', command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=10, pady=5)
        self.done = True
        self.window.mainloop()
        self.window.protocol("WM_DELETE_WINDOW", self.stop)

    def write(self):
        message = f"{self.username}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode("utf-8"))
        self.input_area.delete('1.0', 'end')

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'USER':
                    self.sock.send(self.username.encode('utf-8'))
                else:
                    if self.done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

    def stop(self):
        self.running = False
        self.window.destroy()
        self.sock.close()
        exit(0)


client = Client(HOST, PORT)
