import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv

def scan_port(ip, port, timeout=0.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            return (port, True)
        else:
            return (port, False)
    except socket.gaierror:
        return (port, None)  # IP invalide
    except socket.timeout:
        return (port, None)  # Timeout
    except Exception as e:
        return (port, None)
    finally:
        sock.close()

def main():
    parser = argparse.ArgumentParser(description="Scanner de ports TCP multithreadé")
    parser.add_argument("--ip", required=False, default="127.0.0.1", help="Adresse IP cible (défaut 127.0.0.1)")
    parser.add_argument("--start-port", type=int, default=20, help="Port de début (inclus)")
    parser.add_argument("--end-port", type=int, default=1024, help="Port de fin (inclus)")
    parser.add_argument("--verbose", action="store_true", help="Afficher aussi les ports fermés")
    parser.add_argument("--output", default="scan_results.csv", help="Fichier de sortie CSV (défaut scan_results.csv)")
    parser.add_argument("--threads", type=int, default=100, help="Nombre de threads pour le scan (défaut 100)")
    args = parser.parse_args()

    ip = args.ip
    start_port = args.start_port
    end_port = args.end_port
    verbose = args.verbose
    output_file = args.output
    max_threads = args.threads

    print(f"Scan multithreadé de {ip} de {start_port} à {end_port} avec {max_threads} threads...")

    open_ports = []
    closed_ports = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}

        for future in as_completed(futures):
            port, status = future.result()
            if status is True:
                print(f"[OUVERT] Port {port}")
                open_ports.append(port)
            elif status is False:
                if verbose:
                    print(f"[FERMÉ] Port {port}")
                closed_ports.append(port)
            else:
                if verbose:
                    print(f"[ERREUR] Port {port} : impossible de scanner")

    # Sauvegarde dans un fichier CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['port', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for port in open_ports:
            writer.writerow({'port': port, 'status': 'open'})
        for port in closed_ports:
            writer.writerow({'port': port, 'status': 'closed'})

    print(f"\nScan terminé. Résultats sauvegardés dans {output_file}.")
    print(f"Ports ouverts ({len(open_ports)}): {sorted(open_ports)}")

if __name__ == "__main__":
    main()
