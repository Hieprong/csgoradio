import asyncio
import os
import telnetlib
import threading
import time
import tkinter as tk
from queue import Queue, Empty

import keyboard
import youtube_dl
from pydub import AudioSegment


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def _asyncio_thread(async_loop):
    global ASYNCLOOP
    ASYNCLOOP = async_loop.run_until_complete(listener())


async def listener():
    global PID
    global Csgodir
    global songsearchqueue
    global tn
    global WHITELIST
    global greeting
    global telnetstatus
    global startbutton
    global telneterrorqueue
    global THREADSTOP

    # if greeting == False:
    #     stuff = tn.read_until("Give it a try".encode())
    #
    #     tn.write("exec lelo\n".encode('ascii'))
    #     print('Hello')
    #     greeting = True
    playlist = ["!play".encode(), "!PLAY".encode()]
    while not THREADSTOP:
        PID = threading.get_ident()

        try:
            stuff = tn.expect(playlist)

        except:
            telneterrorqueue.put('The connection was closed by the client')
            startbutton.config(text='Start')
            telnetstatus.config(text="The connection was closed by the client")
            return
        if THREADSTOP == True:
            print("shutdown")
            return

        stuff = stuff[-1].decode('utf_8')

        stuffarray = str(stuff).split("!play".lower())

        cleanstr = stuffarray[0].split("\u200e")

        linkstr = cleanstr[-1].split(" :  ")
        link = linkstr[-1]

        cleanstr.pop()
        nameone = cleanstr[-1].split("\\r\\n")[-1]

        name = nameone.split("\\")[0]
        name = str(name)
        name = name.split("\n")[-1]

        if "(Counter-Terrorist)" in name:
            name = name.replace('(Counter-Terrorist)', "")
            name = name[1:]

        elif "(Terrorist)" in name:
            name = name.replace("(Terrorist)", "")
            name = name[1:]
        if "Empty" in WHITELIST.decode('utf+8') or name in WHITELIST.decode('utf_8').split(";"):
            songsearchqueue.put(link)
            tn.write("-voicerecord\n".encode('ascii'))
            try:
                os.remove('voice_input.mp3')
            except:
                pass
            try:
                os.remove('voice_input')
            except:
                pass
            try:
                os.remove(Csgodir + 'voice_input.wav')
            except:
                pass
            if downloadsong(link) == True:
                currentlyplaying = True
                tn.write("voice_inputfromfile 1\n".encode('ascii'))
                tn.write("+voicerecord\n".encode('ascii'))
                tn.write("voice_scale 1\n".encode('ascii'))
                tn.write("voice_loopback 1\n".encode('ascii'))
            else:
                keyboard.press_and_release('o')
                pass

        else:
            print('A non whitelisted name made a request')


def startlistener(async_loop):
    global songsearchlabel
    global HOST
    global PORT
    global musicthread
    global tn
    global songsearchqueue
    global startbutton
    global telnetstatus
    global started
    global ASYNCLOOP
    global THREADSTOP
    global PID
    global telneterrorqueue
    if os.path.isfile(Csgodir + 'csgo/cfg/csgoradio.cfg'):
        pass
    else:
        try:
            cfgfile = open(Csgodir + 'csgo/cfg/csgoradio.cfg', 'w+')
            cfgfile.write(
                'clear\n// //MUSIC PLAY CUSTOM:\nbind } music_on\nalias music_on \"voice_inputfromfile 1;+voicerecord; voice_loopback 1; bind } music_off\"\nalias music_off \"voice_inputfromfile 0;-voicerecord; voice_loopback 0; bind } music_on\"\nbind l \"say_team Link not found searching youtube...\"\nbind o \"say_team There seems to be an error, please try again\"\nbind k \"voice_inputfromfile 0; voice_loopback 0\"\n// //MUSIC PLAY CUSTOM END.\nclear')
            cfgfile.close()
        except:
            telneterrorqueue.put('Failed to locate Game Installation')

            try:
                telnetstatus.config(text='Failed to locate Game Installation')
            except Empty:
                pass
            return
    try:

        endl = "\n"
        welcome = "CSGO Remote Console Online"

        tn = telnetlib.Telnet(HOST, PORT)
        tn.write("echo Hello \n".encode('ascii'))
        tn.read_until("Hello".encode('ascii'))
        print("Successfully Connected")
        telneterrorqueue.put('Successfully connected')
    except:
        telneterrorqueue.put('Connection could not be established')

        try:
            telnetstatus.config(text=telneterrorqueue.get(False))
        except Empty:
            pass
        return
    if started == False:
        THREADSTOP = False

        musicthread = threading.Thread(target=_asyncio_thread, args=(async_loop,), daemon=True)
        musicthread.start()
        startbutton.config(text='Stop')
        telnetstatus.config(text='Successfully connected')
        started = True
    else:

        THREADSTOP = True
        tn.write("echo !play\n".encode('ascii'))
        tn.close()
        try:
            telnetstatus.config(text='Ready to connect to Telnet on port ' + str(PORT))
            startbutton.config(text="Start")
            started = False
        except:
            print("failed to stop")

    def update_values():

        try:
            songsearchlabel.config(text='Currently searching for: ' + songsearchqueue.get(False))
            telnetstatus.config(text=telneterrorqueue.get(False))
        except Empty:
            pass
        t = threading.Timer(0.250, update_values)
        t.start()

    update_values()


def downloadsong(link):
    global Csgodir
    global NormVol
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'voice_input.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    except:
        try:
            keyboard.press_and_release('l')

            time.sleep(0.005)

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(f"ytsearch:{link}", download=True)['entries'][0]
        except:
            print('Error in search function')
    try:
        time.sleep(1)
        src = 'voice_input.mp3'
        dst = Csgodir + 'voice_input.wav'
        sound = AudioSegment.from_file(src)
        sound = sound.set_frame_rate(22050)
        channels = sound.split_to_mono()
        exporti = channels[0].set_sample_width(2)
        exporti = match_target_amplitude(exporti, NormVol)
        exporti.export(dst, format="wav")
        return True
    except:
        return False


def option_window():
    global ow
    global root
    global Whitelistactive
    global Csgodir
    global HOST
    global PORT
    global NormVol
    global WHITELIST
    if ow is None:

        ow = tk.Toplevel(root)
        ow.geometry('700x300')
        ow.resizable(False, False)
        Csgodiropt = tk.Entry(ow, width=80)
        Csgodiropt.delete(0, 'end')
        Csgodiropt.insert(0, Csgodir)
        csgodirlabel = tk.Label(ow, text='CsGo directory')
        csgodirlabel.grid(row=1, column=1)
        Csgodiropt.grid(row=1, column=2)

        Normvolset = tk.Entry(ow)
        Normvolset.delete(0, 'end')
        Normvolset.insert(0, NormVol)
        Normvollabel = tk.Label(ow, text='Normalization volume in dBFS')
        Normvollabel.grid(row=2, column=1)
        Normvolset.grid(row=2, column=2)

        Hostset = tk.Entry(ow)
        Hostset.delete(0, 'end')
        Hostset.insert(0, HOST)
        Hostlabel = tk.Label(ow, text='Host IP address')
        Hostlabel.grid(row=3, column=1)
        Hostset.grid(row=3, column=2)

        Portset = tk.Entry(ow)
        Portset.delete(0, 'end')
        Portset.insert(0, str(PORT))
        Portlabel = tk.Label(ow, text='Port')
        Portlabel.grid(row=4, column=1)
        Portset.grid(row=4, column=2)

        Whitelistset = tk.Entry(ow, width=80)
        Whitelistset.delete(0, 'end')
        Whitelistset.insert(0, WHITELIST.decode("utf_8"))
        Whitelistlabel = tk.Label(ow, text='Whitelist ;sep')
        Whitelistlabel.grid(row=5, column=1)
        Whitelistset.grid(row=5, column=2)
        Whitelistactive = tk.Label(ow, text="Loading")
        Whitelistactive.grid(row=6, column=2)

        def Whiteliststatus():
            global Whitelistactive
            try:
                WHITELIST = Whitelistset.get().encode('utf-8')
                if "Empty" in WHITELIST.decode('utf_8'):
                    Whitelistactive.config(text="Whitelist contains the word Empty and is disabled")
                else:
                    Whitelistactive.config(text="Whitelist is active")
            except:
                pass
            t = threading.Timer(0.250, Whiteliststatus)
            t.start()

        Whiteliststatus()

        def saveoption():
            global Csgodir
            global NormVol
            global HOST
            global PORT
            global ow
            global WHITELIST
            if Csgodiropt.get()[-1] is not "\\" and Csgodiropt.get()[-1] is not "/":
                Csgodir = Csgodiropt.get().decode("utf_8") + "/"
            else:
                Csgodir = Csgodiropt.get()
            optiondoc = open('CsgoRadiooptions.txt', 'w', encoding="utf_8")
            WHITELISTNAMES = Whitelistset.get().encode("utf_8")
            optiondoc.write('Csgodir =' + Csgodir + '\nNormVol =' + str(
                Normvolset.get()) + '\nHostip =' + Hostset.get() + '\nPort =' + str(
                Portset.get()) + '\nWhitelist =' + WHITELISTNAMES.decode('utf_8') + '\n')
            optiondoc.close()

            NormVol = float(Normvolset.get())
            HOST = Hostset.get()
            PORT = int(Portset.get())
            WHITELIST = Whitelistset.get().encode("utf_8")

            ow.destroy()
            ow = None

        Savebutton = tk.Button(ow, text='Save', command=saveoption)
        Savebutton.grid(row=7, column=2)

    def on_closing():
        global ow
        ow.destroy()
        ow = None

    ow.protocol("WM_DELETE_WINDOW", on_closing)


def main(async_loop):
    global PORT
    global tn
    global root
    global songsearchqueue
    global songsearchlabel
    global startbutton
    global telneterrorqueue
    global telnetstatus
    songsearchqueue = Queue()
    telneterrorqueue = Queue()
    songsearchqueue.put('Empty')
    telneterrorqueue.put('Ready to connect to Telnet on port ' + str(PORT))

    currentlyplaying = False
    greeting = False
    root = tk.Tk()
    root.geometry('400x300')
    root.resizable(False, False)
    startbutton = tk.Button(master=root, text='Start', command=lambda: startlistener(async_loop))
    startbutton.place(x=200, y=270)
    optionbutton = tk.Button(master=root, text='Options', command=option_window)
    songsearchlabel = tk.Label(master=root, text=songsearchqueue.get())
    telnetstatus = tk.Label(master=root, text=telneterrorqueue.get())
    optionbutton.place(x=300, y=270)
    songsearchlabel.pack()
    telnetstatus.pack()

    root.mainloop()


if __name__ == '__main__':
    if os.path.isfile('CsgoRadiooptions.txt'):
        try:

            optiondoc = open('CsgoRadiooptions.txt', "rb")

            options = optiondoc.read().decode("utf_8")

            valuespre = options.split("\n")
            valuespre.pop()

            values = []
            for item in valuespre:
                values.append(item.split('=')[1])

            Csgodir = values[0].rstrip()
            NormVol = float(values[1].rstrip())
            HOST = values[2].rstrip()
            PORT = int(values[3].rstrip())
            WHITELIST = values[4].rstrip()
            WHITELIST = WHITELIST.encode("utf_8")

            optiondoc.close()
        except:
            print('Error loading preferences... Loading default values')
            try:
                optiondoc.close()
            except:
                pass
            optiondoc = open('CsgoRadiooptions.txt', "wb")

            optiondoc.write(
                b'Csgodir =C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/\nNormVol =-60.0\nHostip =127.0.0.1\nPort =2121\nWhitelist =Empty\n')

            Csgodir = 'C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/'
            NormVol = -60.0
            HOST = '127.0.0.1'
            PORT = 2121
            WHITELIST = b"Empty"
            optiondoc.close()
    else:
        optiondoc = open('CsgoRadiooptions.txt', "wb")
        optiondoc.write(
            b'Csgodir =C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/\nNormVol =-60.0\nHostip =127.0.0.1\nPort =2121\nWhitelist =Empty\n')
        Csgodir = 'C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/'
        NormVol = -60.0
        HOST = '127.0.0.1'
        PORT = 2121
        WHITELIST = b"Empty"
        optiondoc.close()

    tn = None
    ow = None
    started = False
    songsearchlabel = None
    songsearchqueue = None
    startbutton = None
    async_loop = asyncio.get_event_loop()
    main(async_loop)
