# Discord Bot Gen

## Description

**Discord-Bot-Gen** est un bot Discord écrit en Python qui permet aux utilisateurs de générer des comptes pour différents services et d'autres fonctionnalités utiles comme la gestion de la réputation des utilisateurs, l'ajout et la suppression de comptes, etc. Le bot est conçu pour être simple à configurer et à utiliser.

## Fonctionnalités

- Génération de comptes pour des services spécifiques.
- Gestion des comptes vérifiés.
- Système de réputation pour suivre l'activité des utilisateurs.
- Commandes administratives pour ajouter et supprimer des comptes.
- Notification automatique pour les nouveaux comptes disponibles.
- Système de feedback pour recueillir les suggestions des utilisateurs.

## Dépendances

Assurez-vous d'installer les dépendances suivantes avant d'exécuter le bot :

- **Python 3.8+**
- `discord.py` (installez avec `pip install discord.py`)
- `json` (inclus par défaut avec Python)
- `logging` (inclus par défaut avec Python)

## Installation des dépendances

Exécutez la commande suivante pour installer les dépendances nécessaires :

```bash
pip install discord.py
Installation
Clonez ce dépôt GitHub :
bash

git clone https://github.com/Komaxtv/Discord-Bot-Gen.git
cd Discord-Bot-Gen
Configurez vos fichiers JSON pour stocker les comptes :
Créez un fichier compte.json pour stocker les comptes générés.
Créez un fichier comptecheck.json pour les comptes vérifiés.
Créez un fichier reputation.json pour suivre la réputation des utilisateurs.
Exemple de fichier compte.json
Voici un exemple de la structure du fichier compte.json :

json

{
  "service_name": [
    {
      "email": "exemple@domaine.com",
      "mdp": "motdepasse123"
    }
  ]
}
Exemple de fichier comptecheck.json
Voici un exemple de la structure du fichier comptecheck.json :

json

{
  "service_name": [
    {
      "email": "verifie@domaine.com",
      "mdp": "motdepasse456"
    }
  ]
}
Exemple de fichier reputation.json
Voici un exemple de la structure du fichier reputation.json :

json

{
  "username": 0
}
Configuration
Ouvrez le fichier Python principal (par exemple bot.py).
Remplacez "VOTRE TOKEN" par le token de votre bot Discord.
Commandes disponibles
Voici les commandes que vous pouvez utiliser avec le bot :

!gen <service> : Génère un compte pour un service spécifique depuis compte.json.
!gencheck <service> : Génère un compte vérifié pour un service depuis comptecheck.json.
!stats : Affiche les statistiques des comptes disponibles.
!addaccount <service> <email> <mdp> : Ajoute un compte à compte.json.
!removeaccount <service> <email> : Supprime un compte de compte.json.
!searchaccount <email> : Recherche un compte par email dans compte.json.
!reputation : Affiche les points de réputation des utilisateurs.
!feedback <message> : Envoie un feedback à l'administrateur du bot.
!helpgen : Affiche la liste des commandes disponibles.
!notificationcompte : Notifie les utilisateurs sur les nouveaux comptes disponibles (administrateur uniquement).
Démarrage du bot
Pour démarrer le bot, exécutez la commande suivante :

bash
python bot.py
Aide et contributions
Si vous avez des questions ou des suggestions, n'hésitez pas à créer une issue sur GitHub. Les contributions sont les bienvenues !

Amusez-vous bien avec le bot ! 🎉
