import telegram as tl
from telegram.ext import *
import logging


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

    dp.add_handler(
        CommandHandler(
            'reset', 
            restart, 
            filters=Filters.user(username = '@esft24')
        )
    )
    dp.add_handler(CommandHandler('buttons', buttons))
    dp.add_handler(CommandHandler('pm', pm))
    dp.add_handler(CallbackQueryHandler(nextB, pass_update_queue=True, pattern="next"))
    dp.add_handler(CallbackQueryHandler(option, pass_update_queue=True))

    updater.start_polling()
    updater.idle()

def build_menu(buttons, n_cols, 
                header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.insert(footer_buttons)
    return menu

def buttons(update, context):
    button_list = [
        tl.InlineKeyboardButton("choice1", 
                                callback_data="Choice 1 selected"),
        tl.InlineKeyboardButton("choice2", 
                                callback_data="Choice 2 selected"),
        tl.InlineKeyboardButton("next", 
                                callback_data="next"),
    ]

    reply_markup = tl.InlineKeyboardMarkup(build_menu(button_list, 
                    n_cols=2))

    context.bot.send_message(chat_id=update.message.chat_id,
                            text="Make your choice",
                            reply_markup=reply_markup)

def option(update, context):
    context.bot.editMessageText(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        text=update.callback_query.data)

def nextB(update, context):
    context.bot.editMessageText(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        text="Next Keyboard")

def pm(update, context):
    context.bot.sendMessage(
        text="PM",
        chat_id=update.message.from_user.id
        )

if __name__ == "__main__":
    logging.basicConfig(format='\n %(asctime)s \n %(name)s \n %(levelname)s \n %(message)s',
                        level=logging.INFO)
    main()
