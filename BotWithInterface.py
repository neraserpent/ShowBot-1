# -*- coding: utf-8 -*-
import config
import telebot
import time
import sys 
import tmdbsimple as tmdb
tmdb.API_KEY = 'ecd5e3611e31538dade6f2a1946d05c0'

reload(sys)
sys.setdefaultencoding('utf-8')
db_states = dict()
db_counters = dict()
db_searchs = dict()
db_lists = dict()
btnBack = telebot.types.KeyboardButton('Back')
btnMenu = telebot.types.KeyboardButton('To Menu')

def listener(messages):
    for m in messages:
        if m.text == '/start':
            db_states.update({m.chat.id: 1})
            hello(m)
        elif db_states.get(m.chat.id) == None:
                    db_states.update({m.chat.id: 1})
                    hello(m)
        elif m.text == 'get':
            command_get(m)
        elif m.text == 'To Menu':
            db_states.update({m.chat.id: 1})
            hello(m)
        elif db_states.get(m.chat.id) == 1:
            if m.text == 'Help':
                command_help(m)
            elif m.text == 'Top...' or m.text == 'Hot...' or m.text == 'Best...':
                db_states.update({m.chat.id: 11})
                command_top(m)
            #SEARCH
            else:
                db_states.update({m.chat.id: 2})
                db_searchs.update({m.chat.id: m.text})
                command_search(m)
                #unknown_command(m)
        elif db_states.get(m.chat.id) == 11:
            if m.text == 'By month' or m.text == 'By year':
                db_states.update({m.chat.id: 111})
                command_period(m)
            elif m.text == 'Back':
                db_states.update({m.chat.id: 1})
                hello(m)
        elif db_states.get(m.chat.id) == 111:
            if m.text == 'Back':
                db_states.update({m.chat.id: 11})
                command_top(m)
            elif m.text == 'Prev':
                command_period_prev(m)
            elif m.text == 'Next':
                command_period_next(m)
            elif m.text == '1' or m.text == '2' or m.text == '3' or m.text == '4' or m.text == '5':
                db_states.update({m.chat.id: 1111})
                series_num = int(m.text) + db_counters.get(m.chat.id)*5 - 1
                series_body = db_lists.get('pop')[series_num]
                #bot.send_message(m.chat.id,'num='+str(series_num)+' len='+str(len(series_list)))
                command_serial(m,series_body)
        elif db_states.get(m.chat.id) == 1111:
            if m.text == 'Back':
                db_states.update({m.chat.id: 111})
                command_period(m)
        elif db_states.get(m.chat.id) == 2:
            if m.text == 'Prev':
                command_search_prev(m)
            elif m.text == 'Next':
                command_search_next(m)
                          
def hello(m):
    markup = generate_markup_menu()
    bot.send_message(m.chat.id, 'Вас приветсвует IMDb-бот. Он поможет Вам \
        найти сериал согласно актуальным для вас критериям. Выберите категорию\
        для начала поиска.', reply_markup=markup)

def command_get(m):
    bot.send_message(m.chat.id, str(m.chat.id)+" "+str(db[m.chat.id]))

def command_help(m):
    markup = generate_markup_menu()
    bot.send_message(m.chat.id, 'Помощь в пути.', reply_markup=markup)

def command_top(m):
    markup = generate_markup_period()
    bot.send_message(m.chat.id, 'За какой период Вы хотите найти сериал?', \
        reply_markup=markup)

def command_period(m):
    markup = generate_markup_serial()
    db_counters.update({m.chat.id: 0})
    series = get_populars()
    bot.send_message(m.chat.id, series, reply_markup=markup)

def command_period_prev(m):
    markup = generate_markup_serial()
    db_counters.update({m.chat.id: db_counters.get(m.chat.id)-1})
    series = get_populars(db_counters.get(m.chat.id))
    bot.send_message(m.chat.id, series, reply_markup=markup)

def command_period_next(m):
    markup = generate_markup_serial()
    db_counters.update({m.chat.id: db_counters.get(m.chat.id)+1})
    series = get_populars(db_counters.get(m.chat.id))
    bot.send_message(m.chat.id, series, reply_markup=markup)

def command_serial(m, series_body):
    markup = generate_markup_seasons()
    message = ''
    #series_body
    message = series_body['name'] + \
        '\nДата выхода первой серии: ' + series_body['first_air_date'] + \
        '\nОписание: '+series_body['overview']
        
    bot.send_message(m.chat.id, message)
    #bot.send_message(m.chat.id, 'Выход первой серии: 17.04.2011\nОписание: Много крови, убийств, насилия и секса. И парочка драконов.\nhttp://www.imdb.com/title/tt0944947/', reply_markup=markup)

def command_search(m):
    markup = generate_markup_serial()
    db_counters.update({m.chat.id: 0})
    result = search_for(m.text)
    bot.send_message(m.chat.id, result, reply_markup=markup)

def command_search_prev(m):
    markup = generate_markup_serial()
    db_counters.update({m.chat.id: db_counters.get(m.chat.id)-1})
    result = search_for(db_searchs.get(m.chat.id), db_counters.get(m.chat.id))
    bot.send_message(m.chat.id, result, reply_markup=markup)

def command_search_next(m):
    markup = generate_markup_serial()
    db_counters.update({m.chat.id: db_counters.get(m.chat.id)+1})
    result = search_for(db_searchs.get(m.chat.id), db_counters.get(m.chat.id))
    bot.send_message(m.chat.id, result, reply_markup=markup)

def generate_markup_menu():
    from telebot import types
    markup = types.ReplyKeyboardMarkup(row_width=1,one_time_keyboard=True)
    btnTop = types.KeyboardButton('Top...')
    btnHot = types.KeyboardButton('Hot...')
    btnBest = types.KeyboardButton('Best...')
    btnHelp = types.KeyboardButton('Help')
    markup.add(btnTop, btnHot, btnBest, btnHelp)
    return markup

def generate_markup_period():
    from telebot import types
    markup = types.ReplyKeyboardMarkup(row_width=1,one_time_keyboard=True)
    btnMonth = types.KeyboardButton('By month')
    btnYear = types.KeyboardButton('By year')
    markup.add(btnMonth, btnYear, btnBack)
    return markup

def generate_markup_serial():
    from telebot import types
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn1 = types.KeyboardButton('1')
    btn2 = types.KeyboardButton('2')
    btn3 = types.KeyboardButton('3')
    btn4 = types.KeyboardButton('4')
    btn5 = types.KeyboardButton('5')
    btnPrev = types.KeyboardButton('Prev')
    btnNext = types.KeyboardButton('Next')
    markup.row(btn1, btn2, btn3, btn4, btn5)
    markup.row(btnPrev, btnNext)
    markup.row(btnBack);
    markup.row(btnMenu);
    return markup

def generate_markup_seasons():
    from telebot import types
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    markup.add(btnBack, btnMenu)
    return markup

def unknown_command(m):
    markup = generate_markup_menu()
    bot.send_message(m.chat.id, 'Неизвестная команда.', reply_markup=markup)

def get_top_rated(counter=0):
    res = tmdb.TV()
    res_top = res.top_rated()['results']
    
def get_populars(counter=0):
    res = tmdb.TV()
    series_message = ''
    res_pop = res.popular()['results']
    total_results = len(res_pop) - 5*counter
    db_lists.update({'pop':res_pop})
    #TODO: добавить обработку выхода за границы res_pop
    if total_results > 5:
        for series_number in range(5):#range(len(res_pop)):
            series_message += str(series_number+1 + 5*counter) + ': ' + \
                res_pop[series_number + 5*counter]['name'] + '\n'
        return series_message
    elif total_results > 0:
        for series_number in range(total_results):
            series_message += str(series_number+1 + 5*counter) + ': ' + \
                res_pop[series_number + 5*counter]['name'] + '\n'
        return series_message
    else:
        return 'Sorry, i\'ve found nothing.'

#TODO: подумать над передачей всех результатов в ф-ю поэтапной печати
def search_for(series_name, counter=0):
    tm_search = tmdb.Search()
    res_search = tm_search.tv(query = series_name)
    total_results = res_search['total_results'] - 5*counter
    res_search = res_search['results']
    db_lists.update({'search':res_search})
    search_message = 'What i\'ve found:\n'
    if total_results > 5:
        for series_number in range(5):
            search_message += str(series_number+1 + 5*counter) + ': ' + \
                res_search[series_number + 5*counter]['name'] + '\n'
        return search_message
    elif total_results > 0:
        for series_number in range(total_results):
            search_message += str(series_number+1 + 5*counter) + ': ' + \
                res_search[series_number + 5*counter]['name'] + '\n'
        return search_message
    #movie_list = ia.search_movie(series_name)
    #if len(movie_list) > 0:
    #        bot.send_message(m.chat.id, 'Which one?')
    #        for movie_number in range(len(movie_list)):
    #                bot.send_message(m.chat.id,
    #                                 str(movie_number) + ': ' +
    #                                 movie_list[movie_number].data['title'])
                    #функция с дальнейшими действиями
    else:
        return 'Sorry, i\'ve found nothing.'

if __name__ == '__main__':
    bot = telebot.TeleBot(config.token)
    bot.set_update_listener(listener)
    bot.polling(none_stop=True)
