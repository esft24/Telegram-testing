import telegram as tl
from telegram.ext import *
import logging
from monster import *

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

if __name__ == "__main__":
    logging.basicConfig(format='\n %(asctime)s \n %(name)s \n %(levelname)s \n %(message)s',
                        level=logging.INFO)
    main()
