# xdImagePlayer

This is a small and fast image player, just play all images under give path. (will walk through all sub path.)

It might also be the player you're looking for.

UI part is PyQt5. Install it by `conda install pyqt`, or by any other package controler.

## Features:
1. Double click to launch full screen mode.
1. Rigth click to for context menu: play, pause, previous, next.
1. Mouse wheel to browser images, and stop the play.
1. Auto do the best fit of image size to dialog.
1. Preload images to maintain the speed when play fast. Also unload images from memory so it could keep playing with huge number of images.

## Get Start
1. Modify value of `path` and `interval` in xdImagePlayer.py
2. ```python ./xdImagePlayer.py```

## TODO:
1. Shuffle the sequence of image to play.
