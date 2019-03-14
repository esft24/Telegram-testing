import telegram as tl
from telegram.ext import *
import logging
from monster import *
import time

def main():
    def stop_and_restart():
        import os, sys
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)
    
    def restart(update, context):
        from threading import Thread
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()
        update.message.reply_text("Hey, I'm back")

    updater = Updater(
        "793965900:AAHxDmCQmK88F3Mjr9ODPOO7_YC3bL_UsTE", 
        use_context=True)

    dp = updater.dispatcher
    jq = updater.job_queue

    # Personal Handlers
    dp.add_handler(CommandHandler('reset', restart, filters=Filters.user(username = '@esft24')))

    # Game Handlers
    dp.add_handler(CommandHandler('start', nocallback))
    dp.add_handler(CommandHandler('newgame', newgame))
    dp.add_handler(CommandHandler('join', join))
    dp.add_handler(CommandHandler('nogame', resetgame))
    dp.add_handler(CommandHandler('startgame', startgame))
    dp.add_handler(CommandHandler('position', nocallback))
    dp.add_handler(CommandHandler('score', nocallback))
    dp.add_handler(CommandHandler('info', nocallback))

    # Query Handlers
    dp.add_handler(CallbackQueryHandler(processChoice, pass_update_queue=True))

    # Message Handlers
    dp.add_handler(MessageHandler(Filters.command, nocallback))
    
    updater.start_polling()
    updater.idle()

# Callbacks

# Default callback for commands no added yet
def nocallback(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                     text="Command not found. Maybe not added yet?")

# Callback for game creation.    
def newgame(update, context):
    if isPrivate(update, context):
        return

    chat_id = update.message.chat_id
    chat_data = context.chat_data
    key = "game_" + str(chat_id)
    if not key in chat_data:
        game = Game()
        game.chat_id = chat_id
        chat_data[key] = game
        context.bot.sendMessage(
            chat_id=chat_id,
            text="Game created. Every player must join the game with the /join command.\nThe game creator can join too and they can start the game with the command /startgame"
        )
    else:
        context.bot.sendMessage(
            chat_id=chat_id,
            text="There is already a game created in this group. Send /resetGame to reset the game's settings and restart."
        )

# Callback for adding a player to the game.
def join(update, context):
    if isPrivate(update, context):
        return

    chat_id = update.message.chat_id
    chat_data = context.chat_data
    key = "game_" + str(chat_id)

    if not key in chat_data:
        context.bot.sendMessage(
            chat_id=chat_id,
            text="There's not a game started in this group yet! Use /newgame to start a game and then join."
        )
        return

    game = chat_data[key]
    user_id = update.message.from_user.id
    user_first_name = update.message.from_user.first_name
    addable = game.checkIfAddable(user_id)
    if addable == 1:
        context.bot.sendMessage(
            chat_id=chat_id,
            text="You are already in this game!"
        )
        return
    elif addable == 2:
        context.bot.sendMessage(
            chat_id=chat_id,
            text="There isn't space for another monster!"
        )
        return

    try:
        context.bot.sendMessage(
            chat_id=user_id,
            text="Hey {}. Welcome! You are in the game!".format(
                user_first_name)
        )
    except:
        context.bot.sendMessage(
            chat_id=chat_id,
            text="{}, I can't send you a private message. Please go to @mseeksm_bot and click 'Start'. Then try to /join again".format(
                user_first_name)
        )
        return

    player_monster = game.addPlayer(user_id, user_first_name)
    context.bot.sendMessage(
        chat_id=user_id,
        text="You are the {} {}.\n{}\nGo find some spooky love!".format(
            player_monster.name,
            player_monster.emoji,
            player_monster.description)
    )
    user_data = context.user_data
    user_data['monster'] = player_monster

# Callback for game deleting.
def resetgame(update, context):
    if isPrivate(update, context):
        return

    print(update.message.chat.__dict__)

    chat_id = update.message.chat_id
    chat_data = context.chat_data
    key = "game_" + str(chat_id)
    if key in chat_data:
        game = chat_data[key]
        game.deletePlayers()
        del game
        chat_data.clear()

    context.bot.sendMessage(
        chat_id=chat_id,
        text="Game destroyed. Create a game with /newgame"
    )

# Callback for game starting.
def startgame(update, context):
    if isPrivate(update, context):
        return

    chat_id = update.message.chat_id
    chat_data = context.chat_data
    key = "game_" + str(chat_id)

    if not key in chat_data:
        context.bot.sendMessage(
            chat_id=chat_id,
            text="There's not a game started in this group yet! Use /newgame to start a game and then join."
        )
        return
    
    game = chat_data[key]

    # if len(game.players) < 3:
    #     context.bot.sendMessage(
    #         chat_id=chat_id,
    #         text="There's not enough players yet! You need 3 players to start the game. {} players so far.".format(
    #             str(len(game.players))
    #         )
    #     )
    #     return

    context.bot.sendMessage(
        chat_id=chat_id,
        text="\U0001F319 The night is approaching! Check our private chat at @mseekm_bot to know more about your monster."
    )

    game.startGame()

    time.sleep(5)
    startround(update, context)

# Auxiliar functions

# Run the start of the round
def startround(update, context):
    chat_id = update.message.chat_id
    chat_data = context.chat_data
    key = "game_" + str(chat_id)
    game = chat_data[key]
    game.startRound()
    playersIds = game.playersIds

    for p in playersIds:
        startroundmessage(context, p, game.fullMoon)
    
    context.job_queue.run_repeating(thinkTimer, 10, context={
                                    "chat_id": chat_id, "game": game,
                                    "bot": context.bot})
    time.sleep(11)
    makeChoice(update, context)

# Send a message of round start to the user
def startroundmessage(context, user_id, fullMoon):
    if fullMoon:
        context.bot.sendMessage(
            chat_id=user_id,
            text="\U0001F315 \U0001F315 \U0001F315 It's Full Moon! \U0001F315 \U0001F315 \U0001F315"
        )

        context.bot.sendMessage(
            chat_id=user_id,
            text="\U0001F315 You have 120 seconds to think about who to date, and who to betray, and who is who, and whatever else you want to think about. After that you will have to choose your date."
        )

        return

    context.bot.sendMessage(
        chat_id=user_id,
        text="\U0001F319 You have 120 seconds to think about who to date, and who to betray, and who is who, and whatever else you want to think about. After that you will have to choose your date."
    )

# Send timing messages to user
def thinkTimer(context):
    job = context.job
    job_context = job.context
    chat_id = job_context["chat_id"]
    game = job_context["game"]
    bot = job_context["bot"]
    if job.interval == 60:
        for p in game.playersIds:
            context.bot.sendMessage(
                chat_id=p,
                text="60 seconds..."
            )
        job.interval = 30
    elif job.interval == 30:
        for p in game.playersIds:
            bot.sendMessage(
                chat_id=p,
                text="30 seconds..."
            )
        job.interval = 25
    else:

        for i in range(5, 0, -1):
           for p in game.playersIds:
                bot.sendMessage(
                    chat_id=p,
                    text=str(i)
                )
           time.sleep(1)
        job.schedule_removal()

# Run the choosing round
def makeChoice(update, context):
    chat_id = update.message.chat_id
    chat_data = context.chat_data
    key = "game_" + str(chat_id)
    game = chat_data[key]
    players = game.players

    for p in players:
        context.bot.send_message(chat_id=p.playerId, text="Make your choice! \U0000FE0F", reply_markup=p.buildChoiceMenu())

def processChoice(update, context):
    print(context.__dict__)

# Check if the user is in a group or in a private chat
def isPrivate(update, context):
    chat_id = update.message.chat_id
    if update.message.chat.type == "private":
        context.bot.sendMessage(
            chat_id=chat_id,
            text="You have to add me to a group and /newgame me there!"
        )
        return True
    return False

if __name__ == "__main__":
    logging.basicConfig(format='\n %(asctime)s \n %(name)s \n %(levelname)s \n %(message)s',
                        level=logging.INFO)
    main()
