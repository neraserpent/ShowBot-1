# -*- coding: utf-8 -*-
import config
import telebot
from imdb import IMDb
ia = IMDb()

def give_me(series_name):
    movie_list = ia.search_movie(series_name)
        if len(movie_list) > 0:
            bot.send_message(m.chat.id, 'Which one?')
                for movie_number in range(len(movie_list)):
                    bot.send_message(m.chat.id,
                                     str(movie_number) + ': ' +
                                     movie_list[movie_number].data['title'])
                    #функция с дальнейшими действиями
                else:
                    bot.send_message(m.chat.id, 'Sorry, i\'ve found nothing.')

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            if m.text[0:7] == u'give me':
                series_name = m.text[8:]
                give_me(series_name)
            #дальнейшие варианты исходной команды
            #elif m.text[] == u''                  
            bot.send_message(m.chat.id, m.text)

            
if __name__ == '__main__' :
    bot = telebot.TeleBot(config.token)
    bot.set_update_listener(listener)
    bot.polling(none_stop=True)
    while True:
        time.sleep(200)
