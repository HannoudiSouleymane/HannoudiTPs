import pandas as pd
import matplotlib.pyplot as plt
import re

def parse_log_file(log_path):
    log_pattern = re.compile(
        r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s-\s-\s'             # IP et séparateurs
        r'\[(?P<datetime>[^\]]+)\]\s'                            # datetime entre []
        r'"(?P<method>\w+)\s(?P<url>[^\s]+)\sHTTP/1\.1"\s'      # méthode, url, HTTP/1.1
        r'(?P<status>\d{3})?\s?'                                 # status (optionnel)
        r'"?(?P<user_agent>[^"]*)"?'
    )

    data = []
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            m = log_pattern.search(line)
            if m and m.group('status') is not None:
                data.append(m.groupdict())

    df = pd.DataFrame(data)
    print(f"[INFO] Nombre total de lignes parsées : {len(df)}")

    # Convertir status en int
    df['status'] = df['status'].astype(int)

    print("[INFO] Aperçu des données extraites :")
    print(df.head())

    return df

def filter_404(df):
    df_404 = df[df['status'] == 404]
    print(f"[INFO] Nombre de lignes avec erreurs 404 : {len(df_404)}")
    print(df_404.head())
    return df_404

def top_5_ips(df_404):
    top_ips = df_404.groupby('ip').size().sort_values(ascending=False).head(5)
    print("[INFO] Top 5 des IPs générant le plus d'erreurs 404 :")
    print(top_ips)
    return top_ips

def plot_top_ips(top_ips):
    plt.figure(figsize=(10,6))
    bars = plt.bar(top_ips.index, top_ips.values, color='tomato')

    plt.title("Top 5 des IPs générant le plus d'erreurs 404")
    plt.xlabel("Adresse IP")
    plt.ylabel("Nombre d'erreurs 404")
    plt.xticks(rotation=45)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig("top5_404_ips.png")
    print("[INFO] Graphique sauvegardé sous 'top5_404_ips.png'")

def main():
    log_path = r"C:\Users\soule\TP1\access.log"  # adapte ce chemin
    df = parse_log_file(log_path)
    df_404 = filter_404(df)
    top_ips = top_5_ips(df_404)
    plot_top_ips(top_ips)

if __name__ == "__main__":
    main()

