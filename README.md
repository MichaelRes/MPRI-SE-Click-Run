# MPRI-SE-Click-Run

Do you want to test your skills in an old school 2D runner ?
Well you're at the right place !

## Running

We use Python 3 to run our game.
If you don't have it already installed you can find it [here](https://www.python.org/downloads/)

Then after you checked all the dependencies you can run the game by typing the
following command in `/etc` :
```
python3 main.py
```
Enjoy !

## Dependencies

First we recommend to use `pip3` in order to install the different python3 packages.

If you're running on Debian (Wheezy and newer) or Ubuntu (Trusty Tahr and newer)
you can install pip3 by typing the following command:
```
sudo apt-get install python3-pip
```
If you're running on CentOS 7 :
```
# First command requires you to have enabled EPEL for CentOS7
sudo yum install python34-setuptools
sudo easy_install pip
```

Then here is the list of used packages and how to install them :
1. Numpy :
```
pip3 install numpy
```
2. Pygame:
```
pip3 install pygame
```

## Documentation
Make sure you can execute the file gen_doc.sh and execute it. The doc is in the
docs repository.
```
chmod +x gen_doc.sh
./gen_doc.sh
```

## Tests
```
pytest tests
```

Authors : Dang-Nhu Hector, Marotte Joseph, Lalanne Clément.

# File explanation for the developers

`.travis.yml`: The Travis descriptor to be able to build tests with Travis.

`gen_doc.sh`:

`LICENSE`:

`README.md`:

`requirements.txt`:


## ressources

### item

### layer0

### layer1

### monster

### player

## src

## tests
