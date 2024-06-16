import socket
import sys

def main():
    # Verifica se o endereço host:port foi fornecido como argumento
    if len(sys.argv) == 1:
        print("Por favor, forneça host:port")
        sys.exit(1)

    # Resolve o endereço string para um endereço UDP
    try:
        host, port = sys.argv[1].split(':')
        port = int(port)
    except ValueError:
        print("Endereço inválido. Use o formato host:port.")
        sys.exit(1)

    # Inicia a escuta por pacotes UDP no endereço fornecido
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (host, port)
        conn.bind(server_address)
    except socket.error as err:
        print(err)
        sys.exit(1)

    # Lê do listener UDP em um loop infinito
    while True:
        try:
            buf, addr = conn.recvfrom(512)
            print("> ", buf.decode())

            # Envia de volta a mensagem via UDP
            conn.sendto(b"Ola UDPclient\n", addr)
        except socket.error as err:
            print(err)
            return

if __name__ == "__main__":
    main()