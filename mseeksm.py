from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import requests
import re
import logging

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    image_url = contents['url']
    return image_url

def bop(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

def cat(bot, update):
    contents = requests.get('http://aws.random.cat/meow').json()
    url = contents['file']
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

def main():
    updater = Updater('789554488:AAEMQ_yhj4dFHqRiCqs0JOeoTowA10h8e50')
    dp = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                        level=logging.INFO)
    dp.add_handler(CommandHandler('perro', bop))
    dp.add_handler(CommandHandler('dog', bop))
    dp.add_handler(CommandHandler('bop', bop))
    dp.add_handler(CommandHandler('gato', cat))
    dp.add_handler(CommandHandler('bip', cat))
    dp.add_handler(CommandHandler('cat', cat))

    dp.add_handler(CommandHandler('truth', truth))
    dp.add_handler(CommandHandler('verdad', truth))
    dp.add_handler(CommandHandler('marico', truth))
    dp.add_handler(CommandHandler('andres', truth))

    # dp.add_handler(CommandHandler('maria', cuaima))
    dp.add_handler(CommandHandler('maduro', maduro))

    dp.add_handler(CommandHandler('stop', bye))

    filterBD = FilterBuenosDias()
    filterescaces = FilterEscaces()
    filtervenezolano = FilterVenezolano()

    dp.add_handler(MessageHandler(
        filtervenezolano & filterescaces, doble))
    dp.add_handler(MessageHandler(filterescaces, escaces))
    dp.add_handler(MessageHandler(filtervenezolano, venezolano))
    dp.add_handler(MessageHandler(filterBD, buenos_dias))

    dp.add_handler(MessageHandler(Filters.command, khe))
    updater.start_polling()
    updater.idle()


def truth(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id, text="Andrés Buelvas es marico")

def bye(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id, text="Buenas Noches")
    update.stop()

def maduro(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id, text="Coñoe'tumadre")

def cuaima(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id, text="Feliz Cumpleañooooooos!!!!")

def buenos_dias(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id, text=u"\U0001F44D"
    )

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def khe(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                             text="Khe?")

def escaces(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Se escribe 'escasez'")

def venezolano(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Se escribe "venezolano". Los gentilicios en castellano no usan mayúsculas; ejemplos: "venezolano", "mexicano", "estadounidense". La confusión viene del inglés que sí las acostumbra; ejemplos: "Venezuelan", "Mexican", "American". Las instancias en que opera "Venezolano" son sólo después de un punto, al inicio de un párrafo o cuando forme parte de un título.')

def doble(bot, update):
    venezolano(bot, update)
    escaces(bot, update)


class FilterBuenosDias(BaseFilter):
    def filter(self, message):
        msg = message.text.lower()
        b = re.search("[bw]u*eno*s*", msg)
        d = re.search("d[iíy]as*", msg)
        if b and d:
            return True
        return False

class FilterEscaces(BaseFilter):
    def filter(self, message):
        msg = message.text.lower().split()
        for m in msg:
            e1 = re.search("h?e[sz][ck]a[scz]e[sz]", m)
            e2 = re.search("^escasez", m)
            if e1:
                if e2:
                    return False
                return True
        return False

class FilterVenezolano(BaseFilter):
    def filter(self, message):
        msg = message.text.split()
        for m in range(1, len(msg)):
            e1 = re.search("^Venezolano", msg[m])
            if e1 and msg[m - 1][-1] != '.':
                return True
        return False
                

if __name__ == "__main__":
    main()
