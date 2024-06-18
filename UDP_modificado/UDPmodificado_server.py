import socket

# Constantes
BUFFER_SIZE = 1024  # Tamanho do buffer para recepção de dados
TIMEOUT = 5         # Tempo limite para esperar por uma resposta em segundos
WINDOW_SIZE = 5     # Tamanho da janela de envio no protocolo de janela deslizante (não utilizado diretamente neste código)

def handle_client(sock, addr, num_messages):
    """Função para lidar com a comunicação de um cliente"""
    print(f"Conectado a {addr}")  # Imprime o endereço do cliente conectado

    received_messages = {}  # Dicionário para armazenar mensagens recebidas
    expected_seq = 0        # Número de sequência esperado
    total_received = 0      # Contador para o total de mensagens recebidas

    while total_received < num_messages:  # Loop até receber todas as mensagens esperadas
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)  # Recebe dados do cliente
            if not data:
                break  # Se não receber dados, encerra o loop
            
            seq_num, message = data.decode('utf-8').split('|', 1)  # Decodifica e separa o número de sequência e a mensagem
            seq_num = int(seq_num)  # Converte o número de sequência para inteiro

            print(" ")
            print(f"Recebido {seq_num} de {addr}: {message.strip()}")  # Imprime a mensagem recebida

            if seq_num == expected_seq:  # Se o número de sequência for o esperado
                print(f"Mensagem esperada recebida: {message.strip()}")  # Imprime que a mensagem esperada foi recebida
                received_messages[seq_num] = message.strip()  # Armazena a mensagem no dicionário
                expected_seq += 1  # Incrementa o número de sequência esperado
                total_received += 1  # Incrementa o total de mensagens recebidas

                # Processa mensagens recebidas em ordem
                while expected_seq in received_messages:  # Enquanto houver mensagens na ordem esperada
                    print(f"Processando mensagem {expected_seq}: {received_messages[expected_seq]}")  # Processa a mensagem
                    del received_messages[expected_seq]  # Remove a mensagem do dicionário
                    expected_seq += 1  # Incrementa o número de sequência esperado

                # Envia ACK para o cliente
                sock.sendto(f"ACK|{seq_num}".encode('utf-8'), addr)  # Envia um ACK para o cliente
            else:
                print(f"Mensagem fora de ordem: {seq_num}, esperando {expected_seq}")  # Mensagem fora de ordem
                # Envia NACK para solicitar retransmissão da mensagem esperada
                sock.sendto(f"NACK|{expected_seq}".encode('utf-8'), addr)  # Envia um NACK para o cliente

        except socket.timeout:
            print("Timeout, retransmitindo última mensagem")  # Timeout ocorreu
            if expected_seq > 0:
                sock.sendto(f"NACK|{expected_seq - 1}".encode('utf-8'), addr)  # Reenvia um NACK para a última mensagem esperada

    sock.close()  # Fecha o socket
    print(f"Conexão encerrada com {addr}")  # Imprime que a conexão foi encerrada

def main():
    """Função principal para configurar e iniciar o servidor"""
    server_address = ('localhost', 12345)  # Endereço e porta do servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP
    sock.bind(server_address)  # Associa o socket ao endereço do servidor
    sock.settimeout(TIMEOUT)  # Define o tempo limite para operações de recepção no socket

    print(f"Servidor UDP modificado escutando em {server_address}")  # Imprime que o servidor está escutando

    num_messages = 1000  # Define o número de mensagens esperadas do cliente
    handle_client(sock, server_address, num_messages)  # Chama a função para lidar com o cliente

if __name__ == "__main__":
    main()
