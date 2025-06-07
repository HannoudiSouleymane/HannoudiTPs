import psutil
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_dashboard():
    clear_screen()
    print("Tapez 'quit' pour quitter\n")
    
    # CPU usage
    cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
    cpu_total = psutil.cpu_percent(interval=None)
    print("=== Utilisation CPU ===")
    for i, percent in enumerate(cpu_per_core, start=1):
        print(f"  Coeur {i}: {percent}%")
    print(f"  Total: {cpu_total}%\n")
    
    # RAM usage
    mem = psutil.virtual_memory()
    print("=== Mémoire RAM ===")
    mem_info = {
        "Totale": mem.total,
        "Utilisée": mem.used,
        "Libre": mem.available
    }
    for label, val in mem_info.items():
        print(f"  {label}: {val / (1024**3):.2f} Go")
    print()
    
    # Disk usage per partition
    print("=== Utilisation disque ===")
    partitions = psutil.disk_partitions(all=False)
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            print(f"  {p.device} ({p.mountpoint}): {usage.percent}% utilisé")
        except PermissionError:
            print(f"  {p.device} ({p.mountpoint}): accès refusé")
    print()
    
    # Network I/O (global)
    net_io = psutil.net_io_counters()
    print("=== Activité réseau globale ===")
    net_io_info = {
        "Octets envoyés": net_io.bytes_sent,
        "Octets reçus": net_io.bytes_recv,
        "Paquets envoyés": net_io.packets_sent,
        "Paquets reçus": net_io.packets_recv,
    }
    for label, val in net_io_info.items():
        if "Octets" in label:
            print(f"  {label}: {val / (1024**2):.2f} Mo")
        else:
            print(f"  {label}: {val}")
    print()
    
    # Network stats per interface
    print("=== Statistiques réseau par interface ===")
    net_if_stats = psutil.net_if_stats()
    net_if_addrs = psutil.net_if_addrs()
    for iface, stats in net_if_stats.items():
        print(f"  Interface: {iface}")
        print(f"    Est active: {'Oui' if stats.isup else 'Non'}")
        print(f"    Vitesse: {stats.speed} Mbps")
        print(f"    Duplex: {stats.duplex}")
        print(f"    MTU: {stats.mtu}")
        addrs = net_if_addrs.get(iface, [])
        for addr in addrs:
            fam = addr.family.name if hasattr(addr.family, 'name') else str(addr.family)
            print(f"    Adresse: {addr.address} ({fam})")
        print()

def main():
    import threading
    stop_event = threading.Event()

    def input_listener():
        while not stop_event.is_set():
            user_input = input()
            if user_input.strip().lower() == "quit":
                stop_event.set()

    thread = threading.Thread(target=input_listener, daemon=True)
    thread.start()

    try:
        while not stop_event.is_set():
            display_dashboard()
            for _ in range(5):
                if stop_event.is_set():
                    break
                time.sleep(1)
    except KeyboardInterrupt:
        pass

    print("\nProgramme terminé proprement.")

if __name__ == "__main__":
    main()
