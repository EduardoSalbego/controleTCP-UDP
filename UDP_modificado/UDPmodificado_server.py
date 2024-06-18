import socket

BUFFER_SIZE = 1024
TIMEOUT = 5
WINDOW_SIZE = 5

def handle_client(sock, addr, num_messages):
    print(f"Conectado a {addr}")

    received_messages = {}
    expected_seq = 0
    total_received = 0

    while total_received < num_messages:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            if not data:
                break
            
            seq_num, message = data.decode('utf-8').split('|', 1)
            seq_num = int(seq_num)

            print(" ")
            print(f"Recebido {seq_num} de {addr}: {message.strip()}")

            if seq_num == expected_seq:
                print(f"Mensagem esperada recebida: {message.strip()}")
                received_messages[seq_num] = message.strip()
                expected_seq += 1
                total_received += 1

                # Processa mensagens recebidas em ordem
                while expected_seq in received_messages:
                    print(f"Processando mensagem {expected_seq}: {received_messages[expected_seq]}")
                    del received_messages[expected_seq]
                    expected_seq += 1

                # Envia ACK para o cliente
                sock.sendto(f"ACK|{seq_num}".encode('utf-8'), addr)
            else:
                print(f"Mensagem fora de ordem: {seq_num}, esperando {expected_seq}")
                # Envia NACK para solicitar retransmissão da mensagem esperada
                sock.sendto(f"NACK|{expected_seq}".encode('utf-8'), addr)

        except socket.timeout:
            print("Timeout, retransmitindo última mensagem")
            if expected_seq > 0:
                sock.sendto(f"NACK|{expected_seq - 1}".encode('utf-8'), addr)

    sock.close()
    print(f"Conexão encerrada com {addr}")

def main():
    server_address = ('localhost', 12345)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    sock.settimeout(TIMEOUT)

    print(f"Servidor UDP modificado escutando em {server_address}")

    num_messages = 1000
    handle_client(sock, server_address, num_messages)

if __name__ == "__main__":
    main()
