import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    return True

# Regex IP simple et testable sur regex101.com :
ip_regex = re.compile(r'\b\d{1,3}(?:\.\d{1,3}){3}\b')

with open('auth.log', 'r') as f:
    lines = f.readlines()

# Normaliser les lignes en minuscules pour éviter les soucis de casse
lines_lower = [line.lower() for line in lines]

# Extraire lignes échouées et réussies
failed_lines = [line for line in lines_lower if "failed password" in line]
success_lines = [line for line in lines_lower if "accepted password" in line]

def extract_valid_ips(lines):
    ips = []
    for line in lines:
        match = ip_regex.search(line)
        if match:
            ip = match.group(0)
            if is_valid_ip(ip):
                ips.append(ip)
    return ips

failed_ips = extract_valid_ips(failed_lines)
success_ips = extract_valid_ips(success_lines)

failed_counter = Counter(failed_ips)
success_counter = Counter(success_ips)

top5_failed = failed_counter.most_common(5)
top5_success = success_counter.most_common(5)

print("Top 5 IPs avec le plus d'échecs de connexion :")
for ip, count in top5_failed:
    print(f"{ip} : {count}")

print("\nTop 5 IPs avec le plus de réussites de connexion :")
for ip, count in top5_success:
    print(f"{ip} : {count}")

# Préparer les données pour le graphique
ips_failed = [ip for ip, _ in top5_failed]
counts_failed = [count for _, count in top5_failed]

ips_success = [ip for ip, _ in top5_success]
counts_success = [count for _, count in top5_success]

# Pour éviter un mismatch, on fait une union des IPs
all_ips = list(set(ips_failed) | set(ips_success))

counts_failed_all = [failed_counter[ip] for ip in all_ips]
counts_success_all = [success_counter[ip] for ip in all_ips]

x = np.arange(len(all_ips))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 7))
bars1 = ax.bar(x - width/2, counts_failed_all, width, label='Échecs')
bars2 = ax.bar(x + width/2, counts_success_all, width, label='Réussites')

ax.set_xlabel('Adresse IP')
ax.set_ylabel("Nombre d'occurrences")
ax.set_title("Comparaison des IPs avec échecs et réussites de connexion")
ax.set_xticks(x)
ax.set_xticklabels(all_ips, rotation=45, ha='right')
ax.legend()

def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(bars1)
autolabel(bars2)

plt.tight_layout()
plt.show()
