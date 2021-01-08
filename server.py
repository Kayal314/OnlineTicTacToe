from datetime import datetime
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

HOST = '192.168.29.220'
PORT = 7560
ADDRESS = (HOST, PORT)
MAX_CONNECTIONS = 2
BUFFER_SIZE = 100
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)
QUIT_CMD = '{quit}'
ENOUGH_PLAYERS = '{enough}'
conn_clients = []
game_state = [0] * 9


def send_to_clients(msg, except_client):
    """
    Send move message to the other player
    :param except_client: the player who made the mode
    :param msg: bytes['utf8']
    :return: None
    """
    for client in conn_clients:
        if client != except_client:
            client.send(msg)


def handle_clients(client):
    """
    handles each client connected to the server
    :param client: Client
    :return: None
    """
    name = client.recv(BUFFER_SIZE).decode('utf8')
    while True:
        try:
            msg = client.recv(BUFFER_SIZE)
            if msg == bytes(QUIT_CMD, "utf8"):
                for i in range(0, 9):
                    game_state[i] = 0
                client.close()
                conn_clients.remove(client)
                name = 'Player ' + name
                print(f"{name} disconnected at {datetime.now().strftime('%H:%M:%S')}")
                break
            else:
                f"""
                update the game status in {game_state}
                """
                index = int(msg.decode('utf8'))
                game_state[index] = int(name)
                tied, has_won, who_won = check_winner(game_state)
                send_to_clients(msg, client)
                if has_won:
                    win_msg = str(who_won) + 'Won'
                    send_to_clients(bytes(win_msg, 'utf8'), None)
                elif tied:
                    send_to_clients(bytes('Draw', 'utf8'), None)

        except Exception as e:
            print("ERROR: ", e)
            break


def wait_for_connection(server):
    f"""
    waits for a maximum of {MAX_CONNECTIONS} clients to join
    to the server
    :param server: Socket
    :return: None
    """
    running = True
    while running:
        try:
            client, address = server.accept()
            conn_clients.append(client)
            if len(conn_clients) == MAX_CONNECTIONS:
                #  if there are 2 players then tell the clients that now the game can start
                send_to_clients(bytes(ENOUGH_PLAYERS, 'utf8'), None)
            print(f"{address} connected to the server at {datetime.now().strftime('%H:%M:%S')}")
            Thread(target=handle_clients, args=(client,)).start()
        except Exception as e:
            print("ERROR: ", e)
            running = False
    print("ERROR: SERVER CRASHED")


def check_winner(board):
    has_won = False
    who_won = 0
    tied = True
    for i in range(0, 7, 3):
        if (board[i] == board[i + 1] == board[i + 2]) and not board[i] == 0:
            who_won = board[i]
            has_won = True
    for i in range(0, 3):
        if (board[i] == board[i + 3] == board[i + 6]) and not board[i] == 0:
            who_won = board[i]
            has_won = True
    if (board[0] == board[4] == board[8] or board[2] == board[4] == board[6]) and not board[4] == 0:
        who_won = board[4]
        has_won = True
    for val in board:
        tied = tied and not val == 0
    return tied, has_won, who_won


if __name__ == '__main__':
    SERVER.listen(MAX_CONNECTIONS)  # listen for 2 connections
    print("[CONNECTING] Waiting for connections ...")
    start_thread = Thread(target=wait_for_connection, args=(SERVER,))
    start_thread.start()
    start_thread.join()
    SERVER.close()
