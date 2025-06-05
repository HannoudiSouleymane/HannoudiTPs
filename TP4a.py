import socket
import argparse
import sys

def scan_ports(ip, start_port, end_port, timeout=1):
    open_ports = []
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
        except socket.gaierror:
            print(f"Erreur : Adresse IP invalide '{ip}'")
            return None
        except socket.timeout:
            # Timeout, considérer port fermé ou non accessible
            pass
        except Exception as e:
            print(f"Erreur réseau lors de la connexion au port {port} : {e}")
        finally:
            sock.close()
    return open_ports

def main():
    parser = argparse.ArgumentParser(description="Scanner de ports TCP simple")
    parser.add_argument("ip", help="Adresse IP à scanner")
    parser.add_argument("start_port", type=int, help="Port de départ")
    parser.add_argument("end_port", type=int, help="Port de fin")

    args = parser.parse_args()

    # Validation rapide des ports
    if args.start_port < 0 or args.start_port > 65535 or args.end_port < 0 or args.end_port > 65535:
        print("Les ports doivent être compris entre 0 et 65535.")
        sys.exit(1)
    if args.start_port > args.end_port:
        print("Le port de départ doit être inférieur ou égal au port de fin.")
        sys.exit(1)

    open_ports = scan_ports(args.ip, args.start_port, args.end_port)
    if open_ports is None:
        sys.exit(1)

    for port in open_ports:
        print(f"Port {port} ouvert")

if __name__ == "__main__":
    main()
