from sys import modules
from time import sleep
from pm import PM
from rtttl_songs import get_rtttl_song_names, get_rtttl_song_by_name

pm = PM()

def main():
    MELODIES = get_rtttl_song_names()
    play_idx = 0
    print('''
Test music!
Press buttons to draw next or previous drawing. 
Press Ctrl-C to exit.
    ''')
    try:
        while True:
            btn = (not pm.btn_l.value()) * 1 + (not pm.btn_r.value()) * 2
            if btn and btn != last_btn:
                if btn == 1:
                    play_idx = play_idx + 1 if play_idx < len(MELODIES) - 2 else 0
                elif btn == 2:
                    play_idx = play_idx - 1 if play_idx else len(play_idx) - 1
                play_name = MELODIES[play_idx]
                print('Playing:', play_name)
                pm.buzzer.play_rtttl(get_rtttl_song_by_name(play_name))
            last_btn = btn
    except KeyboardInterrupt:
        pass
    pm.set_enable(False)
    modules.clear() # make sure we can re-import the example!
    print('''
Done!
Can press Ctrl-D to soft-reset.
    ''')


if __name__ == '__main__':
    main()