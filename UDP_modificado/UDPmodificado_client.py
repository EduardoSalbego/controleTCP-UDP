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

    # Lista de mensagens para enviar
    messages = ["Olá UDP Server\n", "Como vai?\n", "Esta é uma mensagem importante.\n", "Espero que você receba.\n", "Adeus!\n"]
    
    base = 0  # Número de sequência da base da janela
    next_seq_num = 0  # Próximo número de sequência a ser enviado
    acked = [False] * len(messages)  # Lista de confirmações (ACK) para cada mensagem

    while base < len(messages):  # Loop até que todas as mensagens sejam enviadas e confirmadas
        while next_seq_num < base + WINDOW_SIZE and next_seq_num < len(messages):  # Envia mensagens enquanto houver espaço na janela
            send_message(conn, server_address, messages[next_seq_num], next_seq_num)  # Envia a próxima mensagem
            next_seq_num += 1  # Incrementa o número de sequência

        try:
            data, addr = conn.recvfrom(BUFFER_SIZE)  # Tenta receber uma resposta do servidor
            ack, ack_num = data.decode('utf-8').split('|')  # Decodifica e separa a resposta
            ack_num = int(ack_num)  # Converte o número de sequência do ACK para inteiro

            if ack == "ACK":  # Se a resposta for uma confirmação (ACK)
                print(f"Recebido ACK {ack_num}")  # Imprime no console o ACK recebido
                acked[ack_num] = True  # Marca a mensagem como confirmada
                while base < len(messages) and acked[base]:  # Move a base da janela para frente enquanto as mensagens forem confirmadas
                    base += 1
            elif ack == "NACK":  # Se a resposta for uma não confirmação (NACK)
                print(f"Recebido NACK {ack_num}")  # Imprime no console o NACK recebido
                next_seq_num = ack_num  # Reenvia a partir do número de sequência não confirmado
        except socket.timeout:
            print("Timeout, retransmitindo janela")  # Mensagem de timeout
            next_seq_num = base  # Reinicia o envio a partir da base da janela

    conn.close()  # Fecha a conexão do socket
    print("Cliente finalizado")  # Mensagem de finalização do cliente

if __name__ == "__main__":
    main()  # Chama a função principal quando o script é executado
