# QuadFile Version 2

A temporary (or permanent, depending on configuration) file sharing service written in Flask.

# Features

* Automatically remove files that aren't accessed often enough
* Supports all filetypes
* Prevents duplicate filenames
* Works on all platforms (as long as they can use basic JavaScript)
* Both easy to set up and use
* Threaded for effective use of resources
* Color-coded and real-time console log
* Easy to use with most applications, such as ShareX

# Requirements

* Python 3 (Python 2 might work, dunno, i don't test that, don't care either)
* Install flask, currently that should be the only requirement and hopefully forever (``pip install -r requirements.txt``)

# Using the thing

* Clone the repo somewhere
* Do ``cp conf.py.sample conf.py``
* Edit ``conf.py`` so that the information is correct
* If possible, make it listen on ``127.0.0.1`` and then use something like nginx as a reverse proxy. For security purposes
* ``chmod +x run.py`` and then ``./run.py``
* ???
* PROFIT (Hopefully)