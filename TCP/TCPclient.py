import socket
import sys

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

    # Lê da conexão até que uma nova linha seja enviada
    try:
        data = conn.recv(1024)
        print("> ", data.decode('utf-8').strip())
    except socket.error as err:
        print(err)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
