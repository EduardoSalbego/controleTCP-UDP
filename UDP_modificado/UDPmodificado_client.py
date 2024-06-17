import socket
import sys
import time

# Constantes
BUFFER_SIZE = 1024
TIMEOUT = 2
WINDOW_SIZE = 5

def send_message(conn, server_address, message, seq_num):
    conn.sendto(f"{seq_num}|{message}".encode('utf-8'), server_address)
    print(f"Enviando {seq_num}: {message}")

def main():
    if len(sys.argv) == 1:
        print("Por favor, forneça host:port para conectar")
        sys.exit(1)

    try:
        host, port = sys.argv[1].split(':')
        port = int(port)
    except ValueError:
        print("Endereço inválido. Use o formato host:port.")
        sys.exit(1)

    server_address = (host, port)
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.settimeout(TIMEOUT)

    messages = ["Mensagem 1\n", "Mensagem 2\n", "Mensagem 3\n", "Mensagem 4\n", "Mensagem 5\n"]  # Exemplo de mensagens
    num_messages = 1000  # Número total de mensagens a enviar

    # Inicia o cronômetro
    start_time = time.time()

    base = 0
    next_seq_num = 0
    acked = [False] * num_messages

    while base < num_messages:
        while next_seq_num < base + WINDOW_SIZE and next_seq_num < num_messages:
            send_message(conn, server_address, messages[next_seq_num % len(messages)], next_seq_num)
            next_seq_num += 1

        try:
            data, addr = conn.recvfrom(BUFFER_SIZE)
            ack, ack_num = data.decode('utf-8').split('|')
            ack_num = int(ack_num)

            if ack == "ACK":
                print(f"Recebido ACK {ack_num}")
                acked[ack_num] = True
                while base < num_messages and acked[base]:
                    base += 1
            elif ack == "NACK":
                print(f"Recebido NACK {ack_num}")
                next_seq_num = ack_num
        except socket.timeout:
            print("Timeout, retransmitindo janela")
            next_seq_num = base

    conn.close()

    # Finaliza o cronômetro
    end_time = time.time()

    # Calcula o tempo total de envio
    total_time = end_time - start_time
    print(f"Tempo total para enviar {num_messages} mensagens via UDP modificado: {total_time:.4f} segundos")
    print(f"Tempo médio por mensagem: {total_time / num_messages:.6f} segundos")

if __name__ == "__main__":
    main()
