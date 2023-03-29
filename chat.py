import os

import sys

import tkinter as tk

from tkinter import messagebox, simpledialog

import socket

import threading


DEFAULT_PORT = 5555  # Porta padrão do chat


class ChatApp(tk.Tk):


    def __init__(self):

        super().__init__()


        self.title('Chat P2P')

        self.geometry('400x400')

        self.resizable(False,False)


        self.nickname = self.choose_nickname()

        self.destination_ip = self.get_destination_ip()


        self.chat_history = tk.Text(self, width=50, height=20)

        self.chat_history.pack(pady=10)


        self.message_entry = tk.Entry(self, width=30)

        self.message_entry.pack(side=tk.LEFT, padx=10, pady=10)


        self.send_button = tk.Button(self, text='Enviar', command=self.send_message)

        self.send_button.pack(side=tk.LEFT)


        self.receive_thread = threading.Thread(target=self.receive_messages)

        self.receive_thread.start()


        self.protocol('WM_DELETE_WINDOW', self.on_closing)


    def choose_nickname(self):

        nickname = simpledialog.askstring('Nickname', 'Digite seu nickname:')

        return nickname


    def get_destination_ip(self):

        ip_address = simpledialog.askstring('IP de destino', 'Digite o IP de destino:')

        return ip_address


    def send_message(self):

        message = self.message_entry.get()


        if message:

            try:

                socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                socket_obj.connect((self.destination_ip, DEFAULT_PORT))

                socket_obj.sendall(f"{self.nickname}: {message}".encode())

                socket_obj.close()

                self.message_entry.delete(0, tk.END)


            except Exception as e:

                messagebox.showerror('Erro', f'Não foi possível enviar a mensagem: {e}')


    def receive_messages(self):

        try:

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            server_socket.bind(('0.0.0.0', DEFAULT_PORT))

            server_socket.listen()


            while True:

                client_socket, address = server_socket.accept()

                message = client_socket.recv(1024).decode()

                self.chat_history.insert(tk.END, message+'\n')

                client_socket.close()


        except Exception as e:

            messagebox.showerror('Erro', f'Não foi possível receber a mensagem: {e}')


    def on_closing(self):

        if messagebox.askokcancel('Saindo', 'Tem certeza que deseja sair?'):

            self.destroy()



if __name__ == "__main__":

    app = ChatApp()

    app.mainloop()