import re
from collections import Counter
import matplotlib.pyplot as plt

# 1. Ouvrir le fichier auth.log
log_path = r"C:\Users\soule\TP1\auth.log"  # ← adapte ce chemin
with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# 2. Extraire les lignes "Failed password"
failed_lines = [line for line in lines if "Failed password" in line]

# 3. Extraire les adresses IP échouées
ip_regex = re.compile(r'(\d{1,3}(?:\.\d{1,3}){3})')
failed_ips = [ip_regex.search(line).group(1) for line in failed_lines if ip_regex.search(line)]

# 4. Compter les occurrences de chaque IP
failed_counts = Counter(failed_ips)

# 5. Extraire les IPs ayant réussi (bonus)
success_lines = [line for line in lines if "Accepted password" in line]
success_ips = [ip_regex.search(line).group(1) for line in success_lines if ip_regex.search(line)]
success_set = set(success_ips)

# 6. Top 5 des IPs échouées
top_failed = failed_counts.most_common(5)
ips = [ip for ip, count in top_failed]
counts = [count for ip, count in top_failed]

# 7. Couleurs (vert = aussi succès, rouge = seulement échecs)
colors = ["green" if ip in success_set else "red" for ip in ips]

# 8. Affichage graphique avec matplotlib
plt.figure(figsize=(10, 6))
bars = plt.bar(ips, counts, color=colors)

# Ajouter les valeurs au-dessus des barres
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom')

# 9. Mise en forme
plt.title("Top 5 des IPs avec le plus d'échecs de connexion SSH")
plt.xlabel("Adresses IP")
plt.ylabel("Nombre d'échecs")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.legend(handles=[
    plt.Rectangle((0, 0), 1, 1, color="red", label="Échecs uniquement"),
    plt.Rectangle((0, 0), 1, 1, color="green", label="Échecs + Succès")
])
plt.tight_layout()

# 10. Sauvegarder l'image au lieu de l'afficher
plt.savefig("top5_failed_ips.png")
# plt.show()  # Optionnel, à commenter si problème d'affichage
