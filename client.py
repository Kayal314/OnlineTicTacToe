from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class Client:
    """
    for communication with the server
    """
    HOST = '192.168.29.220'
    PORT = 7560
    ADDRESS = (HOST, PORT)
    BUFFER_SIZE = 100
    __QUIT_CMD = '{quit}'
    ENOUGH_PLAYERS = '{enough}'

    def __init__(self, player_num, buttons, other_pl, my_turn, label, made_moves):
        """
        Initialize object and send player number to server
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDRESS)
        self.my_turn = my_turn
        self.label = label
        self.made_moves = made_moves
        self.buttons = buttons
        self.other_pl = other_pl
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.player_num = player_num
        self.send_messages(str(player_num))

    def receive_messages(self):
        """
        receive messages from the server
        :return: None
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFFER_SIZE).decode()
                if msg.__eq__(self.ENOUGH_PLAYERS):
                    self.my_turn[2] = True
                elif len(msg) > 1:
                    if msg.__eq__('Draw'):
                        self.label.config(text='Its a Draw!')
                    elif int(msg[0]) == self.player_num:
                        self.label.config(text='You\'ve won!')
                    else:
                        self.label.config(text='You\'ve lost!')
                    self.my_turn[1] = True
                else:
                    index = int(msg)
                    self.made_moves[index] = True
                    self.buttons[index].config(image=self.other_pl)
                    self.my_turn[0] = True
                    self.label.config(text='Your turn')
            except Exception as e:
                print("[EXCEPTION]", e)
                break

    def send_messages(self, msg):
        """
        send messages to the server
        :param msg: str
        :return: None
        """
        self.client_socket.send(bytes(msg, 'utf8'))
        if msg.__eq__(self.__QUIT_CMD):
            self.client_socket.close()

    def disconnect(self):
        self.send_messages(self.__QUIT_CMD)
