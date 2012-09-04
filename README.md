## What
A (poor man's version) port of Mac's [Alfred App.](http://http://www.alfredapp.com/)  
When Dorothy fires up, start typing in the box. 
As you type, Dorothy will list you installed programs that matches what you've written, as well as allow you to search sites like Wikipedia (and even do some simple calculations!)  
Just press the corresponding shortcut keys on the right to perform the action. 
__the 'W' in the shortcut is for the Windows key. not the actual w key__.

## How to use
Start typing. Press desired shortcut keys to perform an action.  

## Install
Put the files in a folder anywhere on your system. 
You have to tell your OS/WM/DE which keys to launch Dorothy.  
Have your system fire a command when you press a certain key combo.  
For instance, I have this in my openbox config:

    <keybind key="A-g">
        <action name="Execute">
            <execute>python2 ~/scripts/dorothy/dorothy.py</execute>
          </action>
    </keybind>



So whenever I press ALT + g, dorothy fires up.


## Screenshots
![Screenshot](http://i.imgur.com/FOXqB.jpg)
![Screenshot](http://i.imgur.com/UPe3c.jpg)

## Dependencies
Python2. If Dorothy isn't launching, make sure you're using pyhton2, not 3.  
Try this in a terminal:  
*$ python /path/to/dorothy.py*  
if you get syntax errors, it's because your system uses python 3 by default. Do this instead:  
*$ python2 /path/to/dorothy.py*


## Notes
* program still in beta. most of it works.
* needs refactoring?
* __python2__, not python3.

Some screenshots and more info can be found here:
http://crunchbanglinux.org/forums/topic/17149/mmmcrunchbox/




   
