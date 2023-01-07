from telegram.ext import Updater
from telegram.ext import CommandHandler
import requests

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

server_addr = 'http://django-service'

def register(update, context):
    session = requests.Session()
    # check if code was written
    try:
        regkoda = int(update.effective_message.text.split(" ")[1])
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Vnesi kodo")
        return None

    r = session.get(url=server_addr + ':8000/app1/users/' + str(update.effective_chat.id))

    if r.status_code == 200:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Uporabnik že registriran")
        return None
    if r.status_code != 404:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Napaka, poskusi kasneje")
        return None

    r = session.get(url=server_addr + ':8000/app1/regkode/' + str(regkoda) + '/')
    if r.status_code == 404:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Neveljavna koda")
        return None
    if r.status_code != 200:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Napaka, poskusi kasneje")
        return None

    jsondata = {"userID": update.effective_chat.id, "veljavnost": "2022-02-02", "ime": "Test", "opis": "Opis test"}
    r = session.post(url=server_addr + ':8000/app1/users/', json=jsondata)
    if r.status_code == 201:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Uporabnik uspesno registriran")

    r = session.delete(url=server_addr + ':8000/app1/regkode/' + str(regkoda) + '/')
    #context.bot.send_message(chat_id=update.effective_chat.id, text="")
    return None

def filters(update, context):
    # TODO Preveri ali je uporabnik ze registriran
    r = requests.get(url=server_addr + ':8000/app1/users/' + str(update.effective_chat.id))

    if r.status_code == 200:
        context.bot.send_message(chat_id=update.effective_chat.id, text="http://20.246.147.191/filterpage/" + str(update.effective_chat.id) + "/")
        return None
    if r.status_code == 404:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Uporabnik ni registriran")
        return None
    context.bot.send_message(chat_id=update.effective_chat.id, text="Prišlo je do napake, poskusite kasneje")

def main():
    updater = Updater(token='1024063569:AAFV_fy723VkLlQs8qIacdIggM5CCkTasOo', use_context=True)
    dispatcher = updater.dispatcher

    register_handler = CommandHandler('register', register)
    dispatcher.add_handler(register_handler)

    filters_handler = CommandHandler('filters', filters)
    dispatcher.add_handler(filters_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
