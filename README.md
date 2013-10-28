Touchless 3D Tracking
===================

This is based on an original project by [Kyle Mc Donald](https://github.com/kylemcdonald) : http://www.instructables.com/id/DIY-3D-Controller/.

Our slightly adapted setup is documented on my hacklab website [hackens.org)](http://hackens.org/) (in french, I may write english doc if some people are interested in that). All the documentation can be found here : http://hackens.org/Projets/TouchlessTracking **(in french, documentation will be written soon, after some extra tests)**.

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

### Chorizo.py

__(working on)__

A script to play music using chorizo pads as a musical keyboard. See [our website](http://hackens.org/Projets/TouchlessTracking) (french, but vids are available, more coming soon) for infos and demos.

### 3d_view.py

__(working on)__

Same as _colors.py_ but represents the position in real space (cube view) rather than in RGB space.

### Some ideas (TODO List)

* Then, use the previous code as a control interface for your computer, just like Minority Report :)
* Other ideas ? It's up to you :)

## Note about the license

TLDR; I don't give a damn to anything you can do using this code. It would just
be nice to quote where the original code comes from.

* -----------------------------------------------------------------------------
* "THE NO-ALCOHOL BEER-WARE LICENSE" (Revision 42):
* Phyks (webmaster@phyks.me) wrote this file. As long as you retain this notice
* you can do whatever you want with this stuff (and you can also do whatever
* you want with this stuff without retaining it, but that's not cool...). If we
* meet some day, and you think this stuff is worth it, you can buy me a
* <del>beer</del> soda in return.
*																		Phyks
* ------------------------------------------------------------------------------

## Thanks

* `Baltazar` from hackEns for his help to set it up and for the original idea.
* [Kyle Mc Donald](https://github.com/kylemcdonald) for his documentation on his setup
* [PRKTRNIC](http://vimeo.com/68763028) (video in french) for the idea about playing music with chorizo and sausages !
