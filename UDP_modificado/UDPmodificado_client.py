import socket  
import sys    
import time    

# Constantes
BUFFER_SIZE = 1024  # Tamanho do buffer para recepção de dados
TIMEOUT = 2         # Tempo limite para esperar por uma resposta em segundos
WINDOW_SIZE = 5     # Tamanho da janela de envio no protocolo de janela deslizante

def send_message(conn, server_address, message, seq_num):
    """Função para enviar uma mensagem com um número de sequência para o servidor"""
    conn.sendto(f"{seq_num}|{message}".encode('utf-8'), server_address)  # Envia a mensagem codificada com o número de sequência para o endereço do servidor
    print(f"Enviando {seq_num}: {message}")  # Imprime no console a mensagem enviada

def main():
    if len(sys.argv) == 1:
        print("Por favor, forneça host:port para conectar")  # Solicita ao usuário fornecer o endereço do servidor
        sys.exit(1)  # Sai do programa com código de erro 1

    try:
        host, port = sys.argv[1].split(':')  # Separa o argumento host:port
        port = int(port)  # Converte a porta para inteiro
    except ValueError:
        print("Endereço inválido. Use o formato host:port.")  # Mensagem de erro caso o formato esteja errado
        sys.exit(1)  # Sai do programa com código de erro 1

    server_address = (host, port)  # Cria uma tupla com o endereço do servidor
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP
    conn.settimeout(TIMEOUT)  # Define o tempo limite para operações de recepção no socket


    messages = ["Mensagem 1\n", "Mensagem 2\n", "Mensagem 3\n", "Mensagem 4\n", "Mensagem 5\n"]  # Exemplo de mensagens
    num_messages = 1000  # Número total de mensagens a enviar

    # Inicia o cronômetro
    start_time = time.time()

    base = 0  # Número de sequência da base da janela
    next_seq_num = 0  # Próximo número de sequência a ser enviado
    acked = [False] * num_messages  # Lista de confirmações (ACK) para cada mensagem

    while base < num_messages:
        while next_seq_num < base + WINDOW_SIZE and next_seq_num < num_messages:
            send_message(conn, server_address, messages[next_seq_num % len(messages)], next_seq_num)
            next_seq_num += 1

        try:
            data, addr = conn.recvfrom(BUFFER_SIZE)  # Tenta receber uma resposta do servidor
            ack, ack_num = data.decode('utf-8').split('|')  # Decodifica e separa a resposta
            ack_num = int(ack_num)  # Converte o número de sequência do ACK para inteiro

            if ack == "ACK":
                print(f"Recebido ACK {ack_num}")
                acked[ack_num] = True
                while base < num_messages and acked[base]:
                    base += 1
            elif ack == "NACK":  # Se a resposta for uma não confirmação (NACK)
                print(f"Recebido NACK {ack_num}")  # Imprime no console o NACK recebido
                next_seq_num = ack_num  # Reenvia a partir do número de sequência não confirmado
        except socket.timeout:
            print("Timeout, retransmitindo janela")  # Mensagem de timeout
            next_seq_num = base  # Reinicia o envio a partir da base da janela

    conn.close()

    # Finaliza o cronômetro
    end_time = time.time()

    # Calcula o tempo total de envio
    total_time = end_time - start_time
    print(f"Tempo total para enviar {num_messages} mensagens via UDP modificado: {total_time:.4f} segundos")
    print(f"Tempo médio por mensagem: {total_time / num_messages:.6f} segundos")

if __name__ == "__main__":
    main() 
