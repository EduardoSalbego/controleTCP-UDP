import socket
import sys

def handle_connection(conn):
    with conn:
        while True:
            # Lê da conexão até que uma nova linha seja enviada
            data = conn.recv(1024)
            if not data:
                break
            print("> ", data.decode('utf-8').strip())

            # Envia de volta a mensagem para o cliente
            conn.sendall("Olá TCP Client\n".encode('utf-8'))

def main():
    # Verifica se o endereço host:port foi fornecido como argumento
    if len(sys.argv) == 1:
        print("Por favor, forneça host:port")
        sys.exit(1)

    # Resolve o endereço string para um endereço TCP
    try:
        host, port = sys.argv[1].split(':')
        port = int(port)
    except ValueError:
        print("Endereço inválido. Use o formato host:port.")
        sys.exit(1)

    # Inicia a escuta por conexões TCP no endereço fornecido
    try:
        server_address = (host, port)
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(server_address)
        listener.listen(5)
        print(f"Servidor TCP escutando em {host}:{port}")
    except socket.error as err:
        print(err)
        sys.exit(1)

    while True:
        # Aceita novas conexões
        conn, addr = listener.accept()
        print(f"Conexão aceita de {addr}")
        # Trata novas conexões em um thread separado para concorrência
        handle_connection(conn)

if __name__ == "__main__":
    main()
