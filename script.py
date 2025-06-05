
import random

# Liste des mots de passe faibles
mots_de_passe_faibles = [
    "123456", "password", "admin", "123456789", "qwerty", "abc123",
    "letmein", "welcome", "monkey", "football"
]

# Choisir un mot de passe au hasard
mot_a_deviner = random.choice(mots_de_passe_faibles)

# Demander à l'utilisateur combien d'essais sont autorisés
while True:
    try:
        limite_essais = int(input("Entrez le nombre maximum d'essais autorisés : "))
        if limite_essais > 0:
            break
        else:
            print("Veuillez entrer un nombre supérieur à 0.")
    except ValueError:
        print("Veuillez entrer un nombre entier.")

# Variables de suivi
essais = 0
historique = []

print("🔐 Devinez le mot de passe faible sélectionné ! (Tapez 'triche' pour l'afficher)")

# Boucle de jeu
while essais < limite_essais:
    tentative = input(f"Essai {essais+1}/{limite_essais} - Votre proposition : ").strip()

    if tentative.lower() == "triche":
        print(f"⚠️ Le mot de passe est : {mot_a_deviner}")
        continue

    historique.append(tentative)
    essais += 1

    if tentative == mot_a_deviner:
        print(f"\n✅ Bravo ! Vous avez trouvé le mot de passe '{mot_a_deviner}' en {essais} essai(s).")
        break
    else:
        print("❌ Mauvaise réponse.")

# Fin de partie
if tentative != mot_a_deviner:
    print(f"\n❌ Limite atteinte. Le mot de passe était : '{mot_a_deviner}'.")

# Affichage de l'historique
print("\n📝 Historique des tentatives :")
for i, essai in enumerate(historique, 1):
    print(f"{i}. {essai}")
