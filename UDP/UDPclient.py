import socket
import sys
import time

def main():
    # Verifica se o endereço host:port foi fornecido como argumento
    if len(sys.argv) == 1:
        print("Por favor, forneça host:port para conectar")
        sys.exit(1)

    # Resolve o endereço string para um endereço UDP
    try:
        host, port = sys.argv[1].split(':')
        port = int(port)
    except ValueError:
        print("Endereço inválido. Use o formato host:port.")
        sys.exit(1)

    # Estabelece a conexão com o endereço usando UDP
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (host, port)
        print(f"Conectado a {host}:{port}")
    except socket.error as err:
        print(err)
        sys.exit(1)

    # Inicia o cronômetro
    start_time = time.time()

    try:
        # Envia 1000 mensagens para o servidor UDP
        for i in range(1000):
            message = f"Mensagem {i+1}\n"
            conn.sendto(message.encode(), server_address)
            print(f"Enviando mensagem {i+1}...")

            # Aguarda a resposta do servidor (se necessário)
            data, _ = conn.recvfrom(4096)
            print(f"> Resposta do servidor: {data.decode().strip()}")

    except socket.error as err:
        print(err)
    finally:
        # Finaliza o cronômetro
        end_time = time.time()
        conn.close()

        # Calcula o tempo total de envio
        total_time = end_time - start_time
        print(f"Tempo total para enviar 1000 mensagens via UDP: {total_time:.4f} segundos")
        print(f"Tempo médio por mensagem: {total_time / 1000:.6f} segundos")

if __name__ == "__main__":
    main()
