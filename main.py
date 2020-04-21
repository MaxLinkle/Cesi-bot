import discord
import mysql.connector
import random

from discord.ext import commands
from mysql.connector import Error

bot_name = "CESI-Bot"
token = "NzAwMjUzOTMzNjk5ODU4NDky.Xp6qEg.N0hkkgTCC-bSl5PEloB6h1tDLU4"
client = commands.Bot(command_prefix="?")
Client = discord.Client()
client.remove_command('help')


try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="cesibot"
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
    await channel.send("Bonjour ! Je suis CESI-Bot ! Souhaitez-moi la bienvenue !")


@client.command(pass_context=True)
async def help(ctx):
    channel = ctx.channel
    await channel.send("Il n'y a rien ici pour l'instant !")


@client.command(pass_context=True)
async def test(ctx):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT contenu_question FROM questions")
    myresult = mycursor.fetchall()
    channel = ctx.channel
    for x in myresult:
        a = x[0].decode('utf-8')
        await channel.send(a)


@client.command(pass_context=True)
async def quizz(ctx, notion: str):
    channel = ctx.channel
    notionCursor = mydb.cursor()
    notionCursor.execute("SELECT * FROM notions")
    notionResult = notionCursor.fetchall()
    exist = False
    notionId = 0
    for x in notionResult:
        if x[1] == notion:
            exist = True
            notionId = x[0]
    if exist:
        questionCursor = mydb.cursor()
        sql = "SELECT * FROM questions WHERE id_notion = %s"
        questionCursor.execute(sql, (notionId, ))
        questionResult = questionCursor.fetchall()
        questionChoice = random.randint(0, len(questionResult)-1)
        questionId = (questionResult[questionChoice])[0]
        answerCursor = mydb.cursor()
        sql = "SELECT * FROM reponses WHERE id_question = %s"
        answerCursor.execute(sql, (questionId, ))
        answerResult = answerCursor.fetchall()
        question = ""
        for x in questionResult:
            if x[0] == questionId:
                question = x[1].decode('utf-8')
        print(question)
        nb = [":one:", ":two:", ":three:", ":four:"]
        for x in range(4):
            answer = (answerResult[x])[1].decode('utf-8')
            print(answer)
            question += "\n" + nb[x] + " " + answer
        await channel.send(question)


client.run(token)