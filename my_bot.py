import discord
from discord.ext import commands
import json
import random
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("bot_logs.log"),
    logging.StreamHandler()
])


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def load_accounts(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Le fichier {filename} est introuvable.")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Erreur lors du chargement de {filename}. Le format JSON est invalide.")
        return {}

def save_accounts(accounts, filename):
    with open(filename, 'w') as f:
        json.dump(accounts, f, indent=4)
        logging.info(f"Les comptes ont été sauvegardés dans {filename}.")


def load_roles():
    try:
        with open('roles.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_roles(roles):
    with open('roles.json', 'w') as f:
        json.dump(roles, f, indent=4)


def load_reputation():
    try:
        with open('reputation.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_reputation(reputation):
    with open('reputation.json', 'w') as f:
        json.dump(reputation, f, indent=4)

@bot.event
async def on_ready():
    logging.info(f'Bot connecté en tant que {bot.user}')


@bot.command()
async def gen(ctx, service: str):
    accounts = load_accounts('compte.json')

    if service not in accounts or len(accounts[service]) == 0:
        await ctx.send(f"Désolé, aucun compte disponible pour {service}.")
        return

    account = random.choice(accounts[service])
    email = account["email"]
    mdp = account["mdp"]

    embed = discord.Embed(title=f"Compte {service} généré", color=0x00ff00)
    embed.add_field(name="Email", value=email, inline=False)
    embed.add_field(name="Mot de passe", value=mdp, inline=False)

    try:
        await ctx.author.send(embed=embed)
        await ctx.send(f"Le compte {service} a été envoyé en privé.")
        logging.info(f"{ctx.author.name} a généré un compte {service}.")
    except discord.Forbidden:
        await ctx.send("Je ne peux pas vous envoyer de message privé. Assurez-vous que vos MP sont ouverts.")
        return

    
    reputation = load_reputation()
    reputation[ctx.author.name] = reputation.get(ctx.author.name, 0) + 1
    save_reputation(reputation)

    await bot.change_presence(activity=discord.Game(name=f"{ctx.author.name} a généré {service}"))

    accounts[service].remove(account)
    save_accounts(accounts, 'compte.json')


@bot.command()
async def gencheck(ctx, service: str):
    roles = load_roles()
    role_name = roles.get("gencheck", "ezbygen")
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role not in ctx.author.roles:
        await ctx.send(f"Vous devez avoir le rôle {role_name} pour utiliser cette commande.")
        return

    accounts = load_accounts('comptecheck.json')

    if service not in accounts or len(accounts[service]) == 0:
        await ctx.send(f"Désolé, aucun compte disponible pour {service}.")
        return

    account = random.choice(accounts[service])
    email = account["email"]
    mdp = account["mdp"]

    embed = discord.Embed(title=f"Compte {service} généré (vérifié)", color=0xFF0000)
    embed.add_field(name="Email", value=email, inline=False)
    embed.add_field(name="Mot de passe", value=mdp, inline=False)

    try:
        await ctx.author.send(embed=embed)
        await ctx.send(f"Le compte {service} a été envoyé en privé.")
        logging.info(f"{ctx.author.name} a généré un compte vérifié pour {service}.")
    except discord.Forbidden:
        await ctx.send("Je ne peux pas vous envoyer de message privé. Assurez-vous que vos MP sont ouverts.")
        return

    accounts[service].remove(account)
    save_accounts(accounts, 'comptecheck.json')

    
    reputation = load_reputation()
    reputation[ctx.author.name] = reputation.get(ctx.author.name, 0) + 1
    save_reputation(reputation)

@bot.command()
@commands.has_role("admin") 
async def setrole(ctx, command_name: str, role_name: str):
    roles = load_roles()
    roles[command_name] = role_name
    save_roles(roles)
    await ctx.send(f"Le rôle {role_name} a été défini pour la commande {command_name}.")


@bot.command()
async def stats(ctx):
    accounts = load_accounts('compte.json')
    total = 0
    most_service = None
    most_count = 0
    message = "Statistiques des comptes :\n"
    for service, acc_list in accounts.items():
        count = len(acc_list)
        total += count
        message += f"{service}: {count} comptes disponibles\n"
        if count > most_count:
            most_count = count
            most_service = service
    message += f"Total des comptes : {total}\n"
    if most_service:
        message += f"Le service avec le plus de comptes est : {most_service} ({most_count} comptes)\n"
    await ctx.send(message)


@bot.command()
@commands.has_role("admin")  
async def addaccount(ctx, service: str, email: str, mdp: str):
    accounts = load_accounts('compte.json')
    
    if service not in accounts:
        accounts[service] = []

    accounts[service].append({"email": email, "mdp": mdp})
    save_accounts(accounts, 'compte.json')
    
    await ctx.send(f"Compte ajouté avec succès pour {service}.")
    logging.info(f"Nouveau compte ajouté pour {service}: {email}")


@bot.command()
@commands.has_role("admin")  
async def removeaccount(ctx, service: str, email: str):
    accounts = load_accounts('compte.json')
    
    if service not in accounts or not accounts[service]:
        await ctx.send(f"Aucun compte disponible pour {service}.")
        return

   
    account_to_remove = None
    for account in accounts[service]:
        if account["email"] == email:
            account_to_remove = account
            break

    if account_to_remove:
        accounts[service].remove(account_to_remove)
        save_accounts(accounts, 'compte.json')
        await ctx.send(f"Compte supprimé avec succès pour {service}: {email}.")
        logging.info(f"Compte supprimé pour {service}: {email}")
    else:
        await ctx.send(f"Le compte avec l'email {email} n'a pas été trouvé pour {service}.")


@bot.command()
@commands.has_role("admin")  
async def searchaccount(ctx, email: str):
    accounts = load_accounts('compte.json')
    found = False
    for service, acc_list in accounts.items():
        for account in acc_list:
            if account["email"] == email:
                embed = discord.Embed(title=f"Compte trouvé pour {service}", color=0x00FF00)
                embed.add_field(name="Email", value=email, inline=False)
                embed.add_field(name="Mot de passe", value=account["mdp"], inline=False)
                await ctx.author.send(embed=embed)
                found = True
                break
        if found:
            break
    if not found:
        await ctx.send(f"Aucun compte trouvé avec l'email {email}.")


@bot.command()
async def reputation(ctx):
    reputation = load_reputation()
    message = "Classement de réputation :\n"
    for user, points in reputation.items():
        message += f"{user}: {points} points\n"
    await ctx.send(message)


@bot.command()
async def feedback(ctx, *, message: str):
    feedback_channel = bot.get_channel(1287490536856621238)  
    embed = discord.Embed(title="Nouveau Feedback", description=message, color=0x00FFFF)
    embed.add_field(name="Envoyé par", value=ctx.author.mention, inline=False)
    await feedback_channel.send(embed=embed)
    await ctx.send("Merci pour votre feedback !")


@bot.command()
async def helpgen(ctx):
    embed = discord.Embed(title="Liste des Commandes", description="Voici les commandes disponibles pour interagir avec le bot :", color=0x00ff00)

    embed.add_field(name="!gen <service>", value="Génère un compte pour un service spécifique depuis `compte.json`.", inline=False)
    embed.add_field(name="!gencheck <service>", value="Génère un compte vérifié pour un service depuis `comptecheck.json`.", inline=False)
    embed.add_field(name="!stats", value="Affiche les statistiques des comptes disponibles.", inline=False)
    embed.add_field(name="!addaccount <service> <email> <mdp>", value="Ajoute un compte à `compte.json`.", inline=False)
    embed.add_field(name="!removeaccount <service> <email>", value="Supprime un compte de `compte.json`.", inline=False)
    embed.add_field(name="!setrole <command_name> <role_name>", value="Associe un rôle à une commande.", inline=False)
    embed.add_field(name="!searchaccount <email>", value="Recherche un compte par email dans `compte.json`.", inline=False)
    embed.add_field(name="!reputation", value="Affiche les points de réputation des utilisateurs.", inline=False)
    embed.add_field(name="!feedback <message>", value="Envoie un feedback à l'administrateur du bot.", inline=False)
    embed.add_field(name="!notificationcompte", value="Affiche le nombre de comptes disponibles pour chaque service (admin uniquement).", inline=False)

    embed.set_footer(text="Utilisez ces commandes pour interagir avec le bot. Bonne chance !")
    
    await ctx.send(embed=embed)


@bot.command()
@commands.has_role("admin")  
async def notificationcompte(ctx):
    accounts = load_accounts('compte.json') 
    notification_embed = discord.Embed(title="Nouveaux Comptes Disponibles", description="Salut @everyone, voici tous les nouveaux comptes disponibles :", color=0x00FF00)

    for service, acc_list in accounts.items():
        count = len(acc_list)  
        notification_embed.add_field(name=service, value=count, inline=False)

    await ctx.send(embed=notification_embed) 


bot.run("VOTRE TOKEN")
