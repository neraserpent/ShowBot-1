# -*- coding: utf-8 -*-
import config
import telebot
import tmdbsimple as tmdb
tmdb.API_KEY = 'ecd5e3611e31538dade6f2a1946d05c0'
db = dict()
#from imdb import IMDb
#ia = IMDb()

#TODO: подумать над передачей всех результатов в ф-ю поэтапной печати
def search_for(m, series_name, counter=0):
    tm_search = tmdb.Search()
    res_search = tm_search.tv(query = series_name)
    total_results = res_search['total_results']
    res_search = res_search['results']
    search_message = 'What i\'ve found:\n'
    if total_results > 5:
        for series_number in range(5):
            search_message += str(series_number+1 + 5*counter) + ': ' + \
                res_search[series_number + 5*counter]['name'] + '\n'
        bot.send_message(m.chat.id, search_message)
    elif total_results > 0:
        for series_number in range(total_results):
            search_message += str(series_number+1 + 5*counter) + ': ' + \
                res_search[series_number + 5*counter]['name'] + '\n'
        bot.send_message(m.chat.id, search_message)
    #movie_list = ia.search_movie(series_name)
    #if len(movie_list) > 0:
    #        bot.send_message(m.chat.id, 'Which one?')
    #        for movie_number in range(len(movie_list)):
    #                bot.send_message(m.chat.id,
    #                                 str(movie_number) + ': ' +
    #                                 movie_list[movie_number].data['title'])
                    #функция с дальнейшими действиями
    else:
        bot.send_message(m.chat.id, 'Sorry, i\'ve found nothing.')
        
def get_populars(m, counter=0):
    res = tmdb.TV()
    series_message = ''
    res_pop = res.popular()['results'];
    #TODO: добавить обработку выхода за границы res_pop
    for series_number in range(5):#range(len(res_pop)):
        series_message += str(series_number+1 + 5*counter) + ': ' + \
            res_pop[series_number + 5*counter]['name'] + '\n'
    bot.send_message(m.chat.id, series_message)
    
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            if m.text[0:10] == u'search for':
                series_name = m.text[11:]
                search_for(m, series_name)
            #дальнейшие варианты исходной команды
            elif m.text == u'get popular series':
                counter = 0
                db.update({m.chat.id: 11})
                get_populars(m)
            elif m.text == u'next' and db.get(m.chat.id) == 11:
                counter += 1
                get_populars(m, counter)
            elif m.text == u'previous' and db.get(m.chat.id) == 11:
                counter -= 1
                get_populars(m, counter)
            elif m.text == u'back':
                counter = 0
                db.update({m.chat.id: 1})
            bot.send_message(m.chat.id, m.text)

            
if __name__ == '__main__' :
    bot = telebot.TeleBot(config.token)
    bot.set_update_listener(listener)
    bot.polling(none_stop=True)
    while True:
        range(200)
        #time.sleep(200)
    
