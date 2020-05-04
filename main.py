import discord
import mysql.connector
import random

from discord.ext import commands
from mysql.connector import Error

bot_name = "CESI-Bot"
token = "NzAwMjUzOTMzNjk5ODU4NDky.XrAT1A.zhya6EPqMQnaxrleblx9FXoSFbo"
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
async def training(ctx, notion: str):
    channel = ctx.channel
    notionCursor = mydb.cursor()
    notionCursor.execute("SELECT * FROM notions")
    notionResult = notionCursor.fetchall()
    exist = False
    notionId = 0

    for x in notionResult:
        if x[1] == notion.capitalize():
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
                question = "```" + x[1].decode('utf-8') + "```"

        msg = await channel.send(question)
        ch = [":regional_indicator_a:", ":regional_indicator_b:", ":regional_indicator_c:", ":regional_indicator_d:"]
        react = ["\U0001F1E6", "\U0001F1E7", "\U0001F1E8", "\U0001F1E9"]

        for x in range(len(react)):
            await msg.add_reaction(react[x])

        juste = 0
        for x in range(4):
            answer = (answerResult[x])[1].decode('utf-8')
            if (answerResult[x])[2] == 1:
                juste = x
            question += "\n" + ch[x] + " " + answer

        await msg.edit(content=question)

        def check(reaction, user):
            return user == ctx.message.author and (str(reaction.emoji) == react[0] or
                                                   str(reaction.emoji) == react[1] or
                                                   str(reaction.emoji) == react[2] or
                                                   str(reaction.emoji) == react[3])

        reaction, user = await client.wait_for('reaction_add', check=check)
        await msg.clear_reactions()

        if str(reaction.emoji) == react[juste]:
            await msg.edit(content=question + "\n\nBonne réponse ! :white_check_mark:")
        else:
            await msg.edit(content=question + "\n\nMauvaise réponse ! :x:")


@client.command(pass_context=True)
async def test(ctx, notion: str):
    channel = ctx.channel
    notionCursor = mydb.cursor()
    notionCursor.execute("SELECT * FROM notions")
    notionResult = notionCursor.fetchall()
    exist = False
    notionId = 0

    for x in notionResult:
        if x[1] == notion.capitalize():
            exist = True
            notionId = x[0]

    if exist:
        while True:
            msg = await channel.send("```Chargement...```")
            await msg.add_reaction("\U00002705")
            await msg.add_reaction("\U0000274C")
            await msg.edit(content="```Un série de 5 questions vous sera posée, êtes-vous prêt(e) ?```")

            def check(reaction, user):
                return user == ctx.message.author and (str(reaction.emoji) == "\U00002705" or
                                                       str(reaction.emoji) == "\U0000274C")

            reaction, user = await client.wait_for('reaction_add', check=check)
            await msg.delete()

            if str(reaction.emoji) == "\U00002705":
                questionCursor = mydb.cursor()
                sql = "SELECT * FROM questions WHERE id_notion = %s"
                questionCursor.execute(sql, (notionId,))
                questionResult = questionCursor.fetchall()
                answers = []
                correction = []

                for x in range(5):
                    questionChoice = random.randint(0, len(questionResult) - 1)
                    questionId = (questionResult[questionChoice])[0]
                    answerCursor = mydb.cursor()
                    sql = "SELECT * FROM reponses WHERE id_question = %s"
                    answerCursor.execute(sql, (questionId,))
                    answerResult = answerCursor.fetchall()
                    question = ""
                    correctionQuestion = []

                    for i in questionResult:
                        if i[0] == questionId:
                            question = "```" + i[1].decode('utf-8') + "```"
                            correctionQuestion.append(question)

                    msg = await channel.send(question)
                    ch = [":regional_indicator_a:", ":regional_indicator_b:", ":regional_indicator_c:",
                          ":regional_indicator_d:"]
                    react = ["\U0001F1E6", "\U0001F1E7", "\U0001F1E8", "\U0001F1E9"]

                    for i in range(len(react)):
                        await msg.add_reaction(react[i])

                    juste = 0
                    testAnswer = ""
                    correctionAnswer = ""
                    for i in range(4):
                        answer = (answerResult[i])[1].decode('utf-8')
                        testAnswer = ch[i] + " " + answer
                        if (answerResult[i])[2] == 1:
                            juste = i
                            correctionAnswer = ch[i] + " " + answer + " :white_check_mark:"
                        else:
                            correctionAnswer = testAnswer
                        question += testAnswer + "\n"
                        correctionQuestion.append(correctionAnswer)

                    await msg.edit(content=question)

                    def check(reaction, user):
                        return user == ctx.message.author and (str(reaction.emoji) == react[0] or
                                                               str(reaction.emoji) == react[1] or
                                                               str(reaction.emoji) == react[2] or
                                                               str(reaction.emoji) == react[3])

                    reaction, user = await client.wait_for('reaction_add', check=check)
                    await msg.clear_reactions()
                    if str(reaction.emoji) == react[juste]:
                        answers.append(1)
                    else:
                        answers.append(0)
                        if str(reaction.emoji) == react[0]:
                            correctionQuestion[1] = correctionQuestion[1] + " :x:"
                        elif str(reaction.emoji) == react[1]:
                            correctionQuestion[2] = correctionQuestion[2] + " :x:"
                        elif str(reaction.emoji) == react[2]:
                            correctionQuestion[3] = correctionQuestion[3] + " :x:"
                        elif str(reaction.emoji) == react[3]:
                            correctionQuestion[4] = correctionQuestion[4] + " :x:"
                    await msg.delete()
                    questionResult.pop(questionChoice)
                    correction.append(correctionQuestion[0] + "\n" +
                                      correctionQuestion[1] + "\n" +
                                      correctionQuestion[2] + "\n" +
                                      correctionQuestion[3] + "\n" +
                                      correctionQuestion[4] + "\n")
                goodAnswers = answers.count(1)
                msg = await channel.send("```Chargement...```")
                await msg.add_reaction("\U0001F6AA")
                await msg.add_reaction("\U0001F4DD")
                await msg.add_reaction("\U0001F504")
                await msg.edit(content="```Votre résultat :```\n" + str(goodAnswers) + "/5\n\n:door: : Sortir du test\n:memo: : Voir la correction\n:arrows_counterclockwise: : Recommencer le test")

                def check(reaction, user):
                    return user == ctx.message.author and (str(reaction.emoji) == "\U0001F6AA" or
                                                           str(reaction.emoji) == "\U0001F4DD" or
                                                           str(reaction.emoji) == "\U0001F504")

                reaction, user = await client.wait_for('reaction_add', check=check)
                await msg.delete()
                if str(reaction.emoji) == "\U0001F6AA":
                    await channel.send(":arrow_left::door: Vous sortez du test...")
                    break
                elif str(reaction.emoji) == "\U0001F4DD":
                    msgCorrection = ""
                    for x in range(len(correction)):
                        msgCorrection += correction[x]
                    msg = await channel.send("Chargement...")
                    await msg.add_reaction("\U0001F6AA")
                    await msg.edit(content=msgCorrection)

                    def check(reaction, user):
                        return user == ctx.message.author and (str(reaction.emoji) == "\U0001F6AA")

                    reaction, user = await client.wait_for('reaction_add', check=check)
                    await msg.delete()
                    if str(reaction.emoji) == "\U0001F6AA":
                        await channel.send(":arrow_left::door: Vous sortez du test...")
                        break
                elif str(reaction.emoji) == "\U0001F504":
                    continue
            elif str(reaction.emoji) == "\U0000274C":
                await channel.send(":no_entry_sign: Test annulé :no_entry_sign:")
                break


@client.command(pass_context=True)
async def addquestion(ctx, notion: str):
    channel = ctx.channel
    ch = [":regional_indicator_a:", ":regional_indicator_b:", ":regional_indicator_b:", ":regional_indicator_c:"]
    react = ["\U0001F1E6", "\U0001F1E7", "\U0001F1E8", "\U0001F1E9"]
    msg = await channel.send("```Veuillez écrire la question :```")
    res = await client.wait_for('message', check=lambda message: message.author == ctx.author)
    await res.delete()
    await msg.delete()
    msg = await channel.send("```Veuillez indiquer Les 4 différents choix de réponse :```")
    choix = []
    phrase = ""

    for x in range(4):
        res = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        phrase += "\n" + ch[x] + " : " + res.content
        choix.append(res)
        await res.delete()

    await msg.delete()
    msg = await channel.send("```Lequel de ces choix est la bonne réponse ?```")

    for x in range(len(react)):
        await msg.add_reaction(react[x])

    await msg.edit(content=msg + phrase)

    def check(reaction, user):
        return user == ctx.message.author and (str(reaction.emoji) == react[0] or str(reaction.emoji) == react[1] or str(reaction.emoji) == react[2] or str(reaction.emoji) == react[3])

    reaction, user = await client.wait_for('reaction_add', check=check)
    await msg.clear_reactions()
    


client.run(token)