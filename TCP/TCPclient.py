import socket
import sys
import time

def main():
    # Verifica se o endereço host:port foi fornecido como argumento
    if len(sys.argv) == 1:
        print("Por favor, forneça host:port para conectar")
        sys.exit(1)

    # Resolve o endereço string para um endereço TCP
    try:
        host, port = sys.argv[1].split(':')
        port = int(port)
    except ValueError:
        print("Endereço inválido. Use o formato host:port.")
        sys.exit(1)

    # Conecta ao endereço usando TCP
    try:
        conn = socket.create_connection((host, port))
        print(f"Conectado a {host}:{port}")
    except socket.error as err:
        print(err)
        sys.exit(1)

    # Envia uma mensagem para o servidor
    try:
        message = "Olá TCP Server\n"
        conn.sendall(message.encode('utf-8'))
        print("Enviando...")
    except socket.error as err:
        print(err)
        sys.exit(1)

    # Inicia o cronômetro
    start_time = time.time()
    
    # Envia 1000 mensagens para o servidor
    try:
        for i in range(1000):
            message = f"Mensagem {i+1}\n"
            conn.sendall(message.encode('utf-8'))
            print(f"Enviando mensagem {i+1}...")
            
            # Aguarda a resposta do servidor
            data = conn.recv(1024)
            print(" ")

    except socket.error as err:
        print(err)
    finally:
        # Finaliza o cronômetro
        end_time = time.time()
        conn.close()

        # Calcula o tempo total de envio
        total_time = end_time - start_time
        print(f"Tempo total para enviar 1000 mensagens via TCP: {total_time:.4f} segundos")
        print(f"Tempo médio por mensagem: {total_time / 1000:.6f} segundos")

if __name__ == "__main__":
    main()
