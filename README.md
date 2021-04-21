# CsGoRadio
This program uses a local Telnet server created by the CsGo launch option -netconport to read ingame chat messages. If it detects a message of the format "Your selected Song !play" 
it will either use the provided youtube link or search youtube for your phrase e.g. "Skyrim main theme !play".
# Download
You can download the zipped file here: [Download](https://mega.nz/file/2wZBBQYa#5560ZPsie5wa4QXVK3RrRjtF4C5q6sGAoOSVCtj5YLI)
# How to use this program
1. Add "-netconport 2121" to your CsGo launch parameters(If you use a diffrent port than 2121 make sure to also change the port in CsGoRadios settings)
2. Start the CsGoRadio.exe and make sure that the CsGo directory set in the options matches the installation of your game.
3. Join or create a server and start the Bot via the start-button.
4. Type "exec csgoradio" into the CsGo console
# FAQ
## Is this program VAC safe?
The launch option -netconport is an officially supported launch option and will not cause a VAC ban. The program also simulates keystrokes to send chat messages via the cfg file, which is akin to a macro.
The program does NOT try to manipulate RAM. There has been extensive testing of this program using multiple accounts, and no VAC issues have occured. That said the developer does not take any responsibilities for a VAC ban occuring from the use of this program.
##  How do I use the Whitelist system?
The Whitelist under options is of the format "Name1;Name2;Name3". If the Whitelist containts the word "Empty" at any point it will Whitelist everybody. Enter your Name as it appears on Steam without any steam team tags.
## Why does it not detect my CsGo name?
I have made my best effort to make this program use the format "utf-8" and support any characters asscociated with it. You will however find combinations that break the program so have fun finding those.
## Can I speak ingame while the music is playing?
No, but you can press your ingame voice key and "k" afterwards to speak freely again.
## What if I dont have a k on my keybaord?
You can navigate to the Steam\steamapps\common\Counter-Strike Global Offensive\csgo\cfg directory and change the line "bind k "voice_inputfromfile 0; voice_loopback 0"" to a key of your choosing. Make sure to save the file before exiting.
## I have found a Bug and would like to report it?
If the bug is repeatable you can report a bug on Github or you can send me a message on Reddit.
## Why do you use Tkinter or python or do this in that way?
[This is why](https://i.redd.it/hk54ti5n6tk11.png)
# Creddits
Developed by u/Hieprong
Feedback and Testing by Roter_Oktober and Dietmar_Schwarz
