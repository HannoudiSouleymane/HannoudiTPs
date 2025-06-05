import pandas as pd
import re
import matplotlib.pyplot as plt

# Regex adapté au format fourni, user_agent optionnel et sans guillemets obligatoires
log_pattern = re.compile(
    r'(?P<ip>\S+) '                  # IP
    r'\S+ \S+ '                     # ident et user (ignorés)
    r'\[(?P<datetime>[^\]]+)\] '    # datetime
    r'"(?P<method>\S+) '            # méthode HTTP
    r'(?P<url>\S+) '                # url
    r'\S+" '                       # protocole HTTP ignoré
    r'(?P<status>\d{3}) '           # code statut
    r'"?(?P<user_agent>[^"\n]*)"?' # user agent, entre guillemets optionnels
)

def parse_line(line):
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    else:
        return None

def load_log_to_df(filepath):
    parsed_lines = []
    with open(filepath, "r", encoding="utf-8", errors='ignore') as f:
        for line in f:
            parsed = parse_line(line)
            if parsed:
                parsed_lines.append(parsed)
            # Ignorer les lignes malformées silencieusement

    df = pd.DataFrame(parsed_lines)
    df['status'] = pd.to_numeric(df['status'], errors='coerce')  # convertit en int, NaN si impossible
    df = df.dropna(subset=['status'])  # enlever lignes sans status valide
    df['status'] = df['status'].astype(int)
    return df

def main():
    filepath = "access.log"

    df = load_log_to_df(filepath)

    # Filtrer erreurs 404
    df_404 = df[df['status'] == 404]

    # Top 5 IP fautives
    top_ips = df_404['ip'].value_counts().head(5)

    print("Top 5 IPs générant le plus d'erreurs 404 :")
    print(top_ips)

    # Visualisation
    plt.figure(figsize=(10,6))
    top_ips.plot(kind='bar', color='tomato')
    plt.title("Top 5 IPs générant des erreurs 404")
    plt.xlabel("Adresse IP")
    plt.ylabel("Nombre d'erreurs 404")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
