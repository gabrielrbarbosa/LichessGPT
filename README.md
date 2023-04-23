<!--![Terminal Lichess](docs/images/lichess.png)-->

<h1 align="center">
  <img height="200" src="docs/images/logo.png">
  <br>
  Lichess GPT (Lichess in the Terminal)
</h1>

## Example
This experiment aims to demonstrate current state of GPT models playing chess.
In this first release it's suggesting 90% invalid moves and the other 10% are mostly blunders, as seen in the game below.

<p align="center">
  <img src="https://lichess1.org/game/export/gif/white/I2YUGRgY.gif?theme=maple&piece=cburnett" alt="MagnusGPT Game" />
</p>

## Info and requirements
* [Lichess](https://lichess.org/), which means that you need to have a Lichess account
* Only Classical and Rapid games because the Lichess API doesn't allow anything else
* This program uses [SAN](https://en.wikipedia.org/wiki/Algebraic_notation_(chess))-notation, see the [Important](#Important)-section.

## Installation

This package is available on [PyPi](https://pypi.org/project/lichs/), therefore just run:

```
$ pip install lichs
```
and the program will be installed. The next step is to generate a personal API-key.

### How to generate a personal API token

1. [Create a Lichess API token](https://lichess.org/account/oauth/token/create?scopes[]=board:play&description=Lichs+cli+play), log into Lichess if necessary
2. Click the button `Submit` in the lower right corner
3. Copy the token shown in the brown box
4. Jump into your terminal and write `lichs <api_token>` (put your API token instead of `<api_token>`) and run the command. To get this clear, an example would have been `lichs lzRceo5XOUND74Lm`. You should then see a message to confirm that the API token has been saved.
5. Set up your OpenAI [API Keys](https://platform.openai.com/account/api-keys), create a file in lichs directory named "openai.key" and save it. Quite expensive to run, so set and monitor your API key limits with OpenAI!


## Usage

<h1 align="center">
  <img src="docs/images/carbon.png">
</h1>

You start playing by typing the command into your terminal:

```
$ lichs
```

That will take you to the intro screen:

```
Welcome to LichessGPT!

What kind of chess do you want to play?
1. Rapid (10+0)
2. Classical (30+0)

Enter 1 or 2:
```

That should be pretty self-explanatory, you basically choose between Rapid and Classical (the Lichess API doesn't support anything else) by entering either 1 or 2. The timing of the games is also listed there; Rapid is 10min and Classical 30min (without extra-time, I might add support for extra-time later)

When you have input either 1 or 2, the program will start to search after an opponent. It shouldn't take long and the game should start pretty quickly.

```
Searching after opponent...
An opponent was found!
```

Then the program will let you know whether you're the color white or black. After that you will start playing; the program will output the board after every move and ask for your move when it's your turn.

```
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . P . . .
P P P P . P P P
R N B Q K B N R
```
Above is an example of the board displayed.


### Important
When the program asks for your move, you need to input the move in [standard algebraic notation](https://en.wikipedia.org/wiki/Algebraic_notation_(chess)) (SAN). Basically, it specifies <ins>which piece</ins> to move and <ins>to where</ins>. As an example, to move a knight from g1 to f3, you type in **Nf3** (N is for Knight, since King uses K). If you want to learn more, click on the link above.

The program will inform you if you can't make the move you have input.

Support for UCI-notation might get added later.

## Contributions
<a href="https://github.com/Cqsi/lichs/graphs/contributors">
  <img src="https://contributors-img.web.app/image?repo=Cqsi/lichs" />
</a>

See the [CONTRIBUTING.md](CONTRIBUTING.md) file for how to contribute.
