# -*- coding: utf-8 -*-
import config
import telebot
import tmdbsimple as tmdb
tmdb.API_KEY = 'ecd5e3611e31538dade6f2a1946d05c0'
#from imdb import IMDb
#ia = IMDb()

def give_me(m, series_name):
    #movie_list = ia.search_movie(series_name)
    #if len(movie_list) > 0:
    #        bot.send_message(m.chat.id, 'Which one?')
    #        for movie_number in range(len(movie_list)):
    #                bot.send_message(m.chat.id,
    #                                 str(movie_number) + ': ' +
    #                                 movie_list[movie_number].data['title'])
                    #функция с дальнейшими действиями
    #else:
        bot.send_message(m.chat.id, 'Sorry, i\'ve found nothing.')
        
def get_populars(m):
    res = tmdb.TV()
    res_pop = res.popular()['results'];
    while m.text != 'exit':
        for series_number in range(5):#range(len(res_pop)):
            bot.send_message(m.chat.id, str(series_number) + ': ' +
                                        res_pop[series_number]['name'])
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            if m.text[0:7] == u'give me':
                series_name = m.text[8:]
                give_me(m, series_name)
            #дальнейшие варианты исходной команды
            elif m.text[0:18] == u'get popular series':
                get_populars(m)
            bot.send_message(m.chat.id, m.text)

            
if __name__ == '__main__' :
    bot = telebot.TeleBot(config.token)
    bot.set_update_listener(listener)
    bot.polling(none_stop=True)
    while True:
        range(200)
        #time.sleep(200)
    
