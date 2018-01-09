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

`gen_doc.sh`: File needed for the documentation generation.

`LICENSE`: License file.

`README.md`: Readme that you are currently reading.

`requirements.txt`: Requirements for launching the game.


## ressources

`black.png`: A black layer that can be used for tests for example.

`green.png`: A green layer that can be used for tests for example.

`ground_sprite.png`: A ground sprite from Minecraft.

`ground.png`: Another sprite used for the ground from Mario.

`layer2.png`: A layer for the ground with a tree.

`red.png`: A red layer that can be used for tests for example.

### item

`green_shroom.png`: A green mushroom sprite.

`red_shroom.png`: A red mushroom sprite

### layer0

`0.png`: A cloud layer.

`1.png`: Another cloud layer.

### layer1

`0.png`: A hill layer.

`1.png`: Another hill layer.

### monster

#### monster1

`1.png`: A sprite for monster 1.

`2.png`: Another sprite for monster 1.

`3.png`: Another sprite for monster 1.

#### monster2

`1.png`: A sprite for monster 2.

`2.png`: Another sprite for monster 2.

`3.png`: Another sprite for monster 2.

#### monster3

`1.png`: A sprite for monster 3.

`2.png`: Another sprite for monster 3.

#### monster4

`1.png`: A sprite for monster 4.

`2.png`: Another sprite for monster 4.

`3.png`: Another sprite for monster 4.

`4.png`: Another sprite for monster 4.

`5.png`: Another sprite for monster 4.

`6.png`: Another sprite for monster 4.

#### monster5

`1.png`: A sprite for monster 5.

`2.png`: Another sprite for monster 5.

`3.png`: Another sprite for monster 5.

`4.png`: Another sprite for monster 5.

### player

#### luigi

##### big

`ascent.png`: The ascent sprite for big Luigi.

`jump.png`: The jump sprite for big Luigi.

`run0.png`: The first sprite of the run of big Luigi.

`run1.png`: The second sprite of the run of big Luigi.

`run2.png`: The third sprite of the run of big Luigi.

##### small

`ascent.png`: The ascent sprite for small Luigi.

`jump.png`: The jump sprite for small Luigi.

`run0.png`: The first sprite of the run of small Luigi.

`run1.png`: The second sprite of the run of small Luigi.

`run2.png`: he third sprite of the run of small Luigi.

#### mario

##### big

`ascent.png`: The ascent sprite for big Mario.

`jump.png`: The jump sprite for big Mario.

`run0.png`: The first sprite of the run of big Mario.

`run1.png`: The second sprite of the run of big Mario.

`run2.png`: he third sprite of the run of big Mario.

##### small

`ascent.png`: The ascent sprite for small Mario.

`jump.png`: The jump sprite for big small Mario.

`run0.png`: The first sprite of the run of small Mario.

`run1.png`: The second sprite of the run of small Mario.

`run2.png`: he third sprite of the run of small Mario.

#### peach

##### big

`ascent.png`: The ascent sprite for big Peach.

`jump.png`: The jump sprite for big Peach.

`run0.png`: The first sprite of the run of big Peach.

`run1.png`: The second sprite of the run of big Peach.

`run2.png`: he third sprite of the run of big Peach.

##### small

`ascent.png`: The ascent sprite for small Peach.

`jump.png`: The jump sprite for small Peach.

`run0.png`: The first sprite of the run of small Peach.

`run1.png`: The second sprite of the run of small Peach.

`run2.png`: he third sprite of the run of small Peach.

#### toad

##### big

`ascent.png`: The ascent sprite for big Toad.

`jump.png`: The jump sprite for big Toad.

`run0.png`: The first sprite of the run of big Toad.

`run1.png`: The second sprite of the run of big Toad.

`run2.png`: he third sprite of the run of big Toad.

##### small

`ascent.png`: The ascent sprite for small Toad.

`jump.png`: The jump sprite for small Toad.

`run0.png`: The first sprite of the run of small Toad.

`run1.png`: The second sprite of the run of small Toad.

`run2.png`: he third sprite of the run of small Toad.

## src

`best_score.data`: A file on the computer that memorizes the best scores.

`entity.py`: A file the contains the classes for an entity and a moving entity.

`item.py`: A file that manages items.

`main.py`: The main file that launches the game.

`map.py`: A file that manages the map. It also manages the procedural generation.

`monster.py`: A file that manages the monsters.

`player.py`: A file that manage the player.

`replay.py`: A file for handling the replays.

`ressources.py`: A file that provides interactions with the resources.

`score.py`: A score manager.

`test_save`:

### state

Here we enter into the implementation of the state machine of the game.

`__init__.py`: The list of available states.

`state_add_score.py`: The state for adding a score.

`state_best_score.py`: The state for presenting the best scores.

`state_credits.py`: The state for showing the credits.

`state_engine.py`: The state engine that goes from one state to another.

`state_game_over.py`: The state when the game is over.

`state_game_play.py`: The state for playing a game from a certain seed.

`state_game_replay.py`: The state for playing a replay.

`state_game.py`: The state of the game.

`state_main_menu.py`: The state for the main menu.

`state_options.py`: The state for the options.

`state_pause.py`: The state in pause.

## tests

### test_map

`test_consistancy.py`:

`test_gen_double_step.py`:

`test_gen_hole.py`:

`test_gen_one.py`:

`test_gen_platform.py`:

`test_gen_proc.py`:

`test_new_map.py`:

`test_on_the_ground.py`:

`test_randomness.py`:
