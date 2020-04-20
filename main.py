import discord
import mysql.connector

from discord.ext import commands
from mysql.connector import Error

bot_name = "CESI-Bot"
token = "NzAwMjUzOTMzNjk5ODU4NDky.XpgeAw.d7wVxdV7FJ_iTDtLTgi18DCsRIY"
client = commands.Bot(command_prefix="?")
Client = discord.Client()
client.remove_command('help')


try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="goldenwolf"
    )
    if mydb.is_connected():
            db_Info = mydb.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = mydb.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.close()
except Error as e:
    print("Error while connecting to MySQL", e)


@client.event
async def on_ready():
    print("Bot online !")
    print("Name :", bot_name)


@client.event
async def on_guild_join(guild):
    channel = guild.system_channel
    await channel.send("Bonjour ! Je suis CESI-Bot ! Souhaitez-moi la bienvenue ou je vous castre c:")


@client.command(pass_context=True)
async def help(ctx):
    channel = ctx.channel
    await channel.send("Il n'y a rien ici pour l'instant !")


@client.command(pass_context=True)
async def quizz(ctx, theme: str):
    channel = ctx.channel
    if theme == "réseaux":



client.run(token)