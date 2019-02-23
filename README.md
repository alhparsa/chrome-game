# Introduction

This game is based on the [T-Rex Game](http://www.trex-game.skipser.com) available on Chrome. Users can play the game by installing the requirements available in the [requirements.txt](https://github.com/alhparsa/chrome-game/blob/master/requirements.txt) file. We have also embedded a evolution algorithm where the game generates numerous players based on the previous mutation and takes the fittest players and use them for the next set of players.

## Neuroevolution Algorithm

Neuroevolution Algorithm or ANN is a branch of AI which the algorithm uses the fittest population defined by a fitness function to mutate the next set of population with a bit of randomness.

[Neuroevoluion Wikipedia](https://en.wikipedia.org/wiki/Neuroevolution)
[Paper Repro: Deep Neuroevolution](https://towardsdatascience.com/paper-repro-deep-neuroevolution-756871e00a66)
[Dissecting Reinforcement Learning](https://mpatacchiola.github.io/blog/2017/03/14/dissecting-reinforcement-learning-5.html)

## Requirements and running the game

To run the program make sure you have `pip` and `git` installed. Once you have `pip` installed then use the following command to clone the project:

```
git clone http://github.com/alhparsa/chrome-game
```

Once cloning is done, then go to the repository's folder by the using the following command:

```
cd chrome-game
```

Then use `pip` to install all the requirements for this project:
```
pip install -r requirements.txt
```
Once you have all the requirements installed then you can run the program by running the `game.py` file:
```
python game.py
```
