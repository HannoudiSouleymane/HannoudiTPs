import os
import platform
import psutil
import time
import threading

def clear_screen():
    # Detecte le système d'exploitation et efface l'écran
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def display_dashboard():
    while True:
        clear_screen()

        # CPU
        cpu_percents = psutil.cpu_percent(percpu=True)
        cpu_total = psutil.cpu_percent()

        print("=== Utilisation CPU ===")
        for i, pct in enumerate(cpu_percents):
            print(f"  Cœur {i} : {pct}%")
        print(f"  Total  : {cpu_total}%\n")

        # RAM
        mem = psutil.virtual_memory()
        print("=== Mémoire RAM ===")
        print(f"  Totale : {mem.total / (1024**3):.2f} Go")
        print(f"  Utilisée : {mem.used / (1024**3):.2f} Go")
        print(f"  Libre   : {mem.available / (1024**3):.2f} Go\n")

        # Disque
        print("=== Utilisation disque par partition ===")
        partitions = psutil.disk_partitions(all=False)
        for part in partitions:
            try:
                usage = psutil.disk_usage(part.mountpoint)
                print(f"  {part.device} ({part.mountpoint})")
                print(f"    Total : {usage.total / (1024**3):.2f} Go")
                print(f"    Utilisé : {usage.used / (1024**3):.2f} Go")
                print(f"    Libre : {usage.free / (1024**3):.2f} Go")
                print(f"    Pourcentage utilisé : {usage.percent}%\n")
            except PermissionError:
                print(f"  {part.device} ({part.mountpoint}) : Permission refusée\n")

        # Activité réseau globale
        net_io = psutil.net_io_counters()
        print("=== Activité réseau globale ===")
        print(f"  Octets envoyés   : {net_io.bytes_sent}")
        print(f"  Octets reçus     : {net_io.bytes_recv}")
        print(f"  Paquets envoyés  : {net_io.packets_sent}")
        print(f"  Paquets reçus    : {net_io.packets_recv}\n")

        # Statistiques par interface
        print("=== Statistiques réseau par interface ===")
        net_if_addrs = psutil.net_if_addrs()
        net_if_stats = psutil.net_if_stats()
        net_if_io = psutil.net_io_counters(pernic=True)

        for iface in net_if_addrs:
            print(f"Interface : {iface}")
            stats = net_if_stats.get(iface)
            io = net_if_io.get(iface)

            if stats:
                print(f"  Status : {'UP' if stats.isup else 'DOWN'}")
                print(f"  Vitesse : {stats.speed} Mbps")
            if io:
                print(f"  Octets envoyés  : {io.bytes_sent}")
                print(f"  Octets reçus    : {io.bytes_recv}")
                print(f"  Paquets envoyés : {io.packets_sent}")
                print(f"  Paquets reçus   : {io.packets_recv}")
            print()

        print("Tapez 'quit' pour quitter.")

        # Attend 5 secondes ou sortie via input dans un thread séparé
        for _ in range(5):
            time.sleep(1)
            if stop_flag.is_set():
                return

def input_listener():
    while True:
        cmd = input()
        if cmd.strip().lower() == "quit":
            stop_flag.set()
            break

if __name__ == "__main__":
    import threading

    stop_flag = threading.Event()
    input_thread = threading.Thread(target=input_listener, daemon=True)
    input_thread.start()

    display_dashboard()

    print("Programme arrêté proprement.")
