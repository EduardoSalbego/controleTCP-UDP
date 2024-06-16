import socket
import sys

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
    except socket.error as err:
        print(err)
        sys.exit(1)

    # Envia uma mensagem para o servidor
    try:
        message = "Ola UDPserver\n"
        conn.sendto(message.encode(), server_address)
        print("enviando...")
    except socket.error as err:
        print(err)
        sys.exit(1)

    # Lê da conexão até que uma nova linha seja enviada
    try:
        data, _ = conn.recvfrom(4096)
        print("> ", data.decode().strip())
    except socket.error as err:
        print(err)
        sys.exit(1)

if __name__ == "__main__":
    main()