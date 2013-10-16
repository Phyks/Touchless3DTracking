Touchless 3D Tracking
===================
----

This is based on an original project by [Kyle Mc Donald](https://github.com/kylemcdonald) : http://www.instructables.com/id/DIY-3D-Controller/.

Our slightly adapted setup is documented on my hacklab website [hackens.org](http://hackens.org/). All the documentation can be found here : **(documentation to be written)**.

In this repository, you'll find :

- A script to upload on the Arduino (we used an Arduino Uno) in the touchless_tracking folder
- Some python scripts to play with it on your computer

## Arduino script

Basically, the Arduino script reads discharge times for the three electrodes (this time is related to the distance between your hand and the electrode). 
It returns formatted lines on the Serial output like the following line :

```
value1␣value2␣value3␣\n
```

where `value1`, `value2`, `value3` are values directly proportional to the discharge time for the electrode (see the code for more infos).

## Python scripts

You'll also find some basic Python scripts as examples on possible use of the setup.

### Colors.py

This script represents the position of your hand in the RGB space. You can then pick a color by placing your hand at a specific point in the box of the electrodes.

### Some ideas (TODO List)

* Same as colors.py but representing it with a 3D view.
* Then, use the previous code as a control interface for your computer, just like Minority Report :)
* Other ideas ? It's up to you :)

## Note about the license
# ============================================================================
# All the scripts in this repository are released under a very permissive 
# license. To make a long story short : do whatever you want with these 
# scripts (but try to have fun :), I don't mind. It would be cool to quote
# the origin of the script if you reuse it, but you don't have to. I'd like to
# be noticed of what you did cool with it (if you think it's worth). :)
# Ah, I almost forgot : If by chance we ever meet and you think this script is
# worth, you can buy me a soda :)
#
#                                                                   Phyks
# =============================================================================  
