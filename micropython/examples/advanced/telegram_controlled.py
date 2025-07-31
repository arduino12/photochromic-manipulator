from sys import modules
from time import sleep_ms
from pm import PM
from rtttl_songs import get_rtttl_song_names
from utils import wifi_connect
from telegram_bot import Bot, ReplyKeyboardMarkup, KeyboardButton as KB
from secrets import *
try:
    from examples.advanced.test_draw import Draw
except ImportError:
    Draw = None


HELP_TEXT = \
'''
/start: get menu keyboard.
/help: print this help message.
'''

ABOUT_TEXT = \
'''
Written by https://github.com/arduino12 2024.
https://mada.org.il/.
'''

g_octave = 4
g_menu = 'main'
g_light = '⚫'
g_melody = 0

kb_main = ReplyKeyboardMarkup([
    (KB('💡'), KB('🔈'), KB('🎹'), KB('📝'), KB('🌡'), KB('⏰')),
    (KB('⚙'),),
    (KB('📖'),),
])

kb_light = ReplyKeyboardMarkup((
    (KB('💡 Light Mode: ⚫'),),
    (KB('⚫'), KB('🔴'), KB('🟡'), KB('🟢'), KB('🔵'), KB('🟣'), KB('⚪')),
    (KB('🚔'), KB('🌈'), KB('🥳'), KB('🔥')),
    (KB('🔙'),),
))

kb_melody = ReplyKeyboardMarkup((
    (KB('🔈 Melody Name'),),
    (KB('⏮'), KB('⏯'), KB('⏭')),
    (KB('♩'), KB('♪'), KB('♫'), KB('♬')),
    (KB('🔙'),),
))

kb_piano = ReplyKeyboardMarkup((
    (KB('🎹 Piano octave 4'),),
    (KB('🔻'), KB('🈴'), KB('🈺'), KB(' '), KB('🈯'), KB('🈳'), KB('♓'), KB('🔺')),
    (KB('🟥'), KB('🟧'), KB('🟨'), KB('🟩'), KB('🟦'), KB('🟪'), KB('🟫')),
    (KB('🔙'),),
))

kb_draw = ReplyKeyboardMarkup((
    (KB('↖️'), KB('⬆️'), KB('↗️')),
    (KB('⬅'), KB('⏹️'), KB('➡')),
    (KB('↙️'), KB('⬇️'), KB('↘️')),
    (KB('🔙'),),
))

kb_drawings = ReplyKeyboardMarkup((
    (KB('⚛'), KB('🇮🇱'), KB('🎗')),
    (KB('🔙'),),
))

pm = PM()
draw = None if Draw is None else Draw(pm)
wifi_connect(WIFI_SSID, WIFI_PASS)
bot = Bot(TELEGRAM_BOT_TOKEN)
MELODIES = get_rtttl_song_names()
WEATHER_EMOJI = '❄🌧☁🌥⛅🌤☀'
# bot.send_message(TELEGRAM_USER_IDS[0], 'Hi♥', reply_markup=kb_piano)


def _update_menu(update, m=None):
    global g_menu
    if m:
        g_menu = m

    kb = globals()['kb_{}'.format(g_menu)]

    if g_menu == 'light':
        kb.data['keyboard'][0][0]['text'] = '💡 Light Mode: {}'.format(g_light)
    elif g_menu == 'melody':
        kb.data['keyboard'][0][0]['text'] = '🔈 Melody: {}'.format(MELODIES[g_melody])
    elif g_menu == 'piano':
        kb.data['keyboard'][0][0]['text'] = '🎹 Piano octave {}'.format(g_octave)

    update.reply(g_menu, reply_markup=kb)


def play_note(n):
    pm.buzzer.beep(440 * (2 ** ((g_octave * 12 + n - 48) / 12)), -100)

def play_melody():
    pm.buzzer.play_rtttl_song(MELODIES[g_melody]) # crush if blocking=False :(

def set_light(update, t):
    global g_light

    g_light = t

    if t == '⚫':
        pm.rgb_leds.fill('black')
    elif t == '🔴':
        pm.rgb_leds.fill('red')
    elif t == '🟡':
        pm.rgb_leds.fill('yellow')
    elif t == '🟢':
        pm.rgb_leds.fill('green')
    elif t == '🔵':
        pm.rgb_leds.fill('blue')
    elif t == '🟣':
        pm.rgb_leds.fill('magenta')
    elif t == '⚪':
        pm.rgb_leds.fill('white')
    _update_menu(update)


@bot.add_command_handler('help')
def help(update):
    print('help')
    update.reply(HELP_TEXT, reply_markup=kb_main)


@bot.add_command_handler('start')
def start(update):
    print('start')
    update.reply('Started', reply_markup=kb_main)


@bot.add_message_handler('')
def cb(update):
    global g_octave, g_melody
    t = update.message['text']
    print(t)

    if t == '🔙':
        _update_menu(update, 'main')
    elif t == '💡':
        _update_menu(update, 'light')
    elif t == '🔈':
        _update_menu(update, 'melody')
    elif t == '🎹':
        _update_menu(update, 'piano')
    elif t == '📝':
        _update_menu(update, 'draw')
    elif t == '📖':
        _update_menu(update, 'drawings')
    elif t == '⚫':
        set_light(update, t)
    elif t == '🔴':
        set_light(update, t)
    elif t == '🟡':
        set_light(update, t)
    elif t == '🟢':
        set_light(update, t)
    elif t == '🔵':
        set_light(update, t)
    elif t == '🟣':
        set_light(update, t)
    elif t == '⚪':
        set_light(update, t)
    elif t == '🟥':
        play_note(0)
    elif t == '🈴':
        play_note(1)
    elif t == '🟧':
        play_note(2)
    elif t == '🈺':
        play_note(3)
    elif t == '🟨':
        play_note(4)
    elif t == '🟩':
        play_note(5)
    elif t == '🈯':
        play_note(6)
    elif t == '🟦':
        play_note(7)
    elif t == '🈳':
        play_note(8)
    elif t == '🟪':
        play_note(9)
    elif t == '♓':
        play_note(10)
    elif t == '🟫':
        play_note(11)
    elif t == '🔻':
        if g_octave > 1:
            g_octave -= 1
            _update_menu(update)
    elif t == '🔺':
        if g_octave < 7:
            g_octave += 1
            _update_menu(update)
    elif t == '⏮':
        g_melody = (g_melody - 1) % len(MELODIES)
        _update_menu(update, 'melody')
        play_melody()
    elif t == '⏯':
        play_melody()
    elif t == '⏭':
        g_melody = (g_melody + 1) % len(MELODIES)
        _update_menu(update, 'melody')
        play_melody()
    elif t == '🚔':
        pm.draw_rect(0, 40, 20)
        pm.move_home()
    elif t == '🌈':
        pm.draw_circle(0, 40, 10)
        pm.move_home()
    elif t == '🥳':
        pm.draw_regular_poly(0, 40, 16, 3)
        pm.move_home()
    elif t == '🔥':
        pm.draw_regular_poly(0, 40, 16, 6)
        pm.move_home()
    elif t == '🌡':
        temp = int(pm.thermometer.read_temp_c())
        update.reply('Temperature: {:02d}°C {}'.format(
            temp, WEATHER_EMOJI[0 if temp <= 20 else 6 if temp >= 30 else int((temp-20) / 2)]),
            reply_markup=kb_main)
    elif t == '⚛':
        if draw is not None:
            draw.mabat_logo()
    elif t == '🇮🇱':
        if draw is not None:
            draw.israel_flag()
    elif t == '🎗':
        if draw is not None:
            draw.yellow_ribbon()


print('''
Telegram-Bot controlled:
Control all hardware via Telegram chat with this bot.
Press Ctrl+C to exit.
''')
try:
    while True:
        bot.update()
        sleep_ms(10)
except KeyboardInterrupt:
    pass
pm.set_enable(False)
modules.clear() # make sure we can re-import the example!
print('''
Done!
Can press Ctrl-D to soft-reset.
''')
