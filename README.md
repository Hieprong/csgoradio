# CsGoRadio
This program uses a local Telnet server created by the CsGo launch option -netconport to read ingame chat messages. If it detects a message of the format "Your selected Song !play" 
it will either use the provided youtube link or search youtube for your phrase e.g. "Skyrim main theme !play".
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
The Whitelist under options is of the format "Name1;Name2;Name3". If the Whitelist containts the word "Empty" at any point it will Whitelist everybody.
## Why does it not detect my CsGo name?
I have made my best effort to make this program use the format "utf-8" and support any characters asscociated with it. You will however find combinations that break the program so have fun finding those.

## I have found a Bug and would like to report it?
