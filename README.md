# Align-Five

## Introduction
This is a two player game, where the users play 
either black or white stones. The objective of the game
is to align 5 stones of the same colour in one row,
column or across a diagonal. Players take alternating
turns to place their stones on the board.
The game is played on a 19 x 19 Go board.

### Getting started with the package
To get started with this package, clone the repo
```bash
git clone https://github.com/mwolinska/Align-Five
```
Then make sure you are in teh right folder
```bash
cd Align-Five
```

Then set up and activate the virtual environment
```bash
python3 -m venv ./venv
source venv/bin/activate
```

Finally, install all the dependencies.
```bash
pip3 install -r requirements.txt
```

### Using the package
An example run would look like this.
First, a clean board is displayed. 

<img src="./Images/GameScreenshots/clean_board.png" height="200">

The first move is made by the user playing white. 

<img src="./Images/GameScreenshots/first_move.png" height="200">

Then the users alternate to play their moves until one of 
the four outcomes is achieved
* 5 stones of one colour are aligned in a row

<img src="./Images/GameScreenshots/win_in_row.png" height="200">

* 5 stones of one colour are aligned in a column

<img src="./Images/GameScreenshots/win_in_column.png" height="200">

* 5 stones of one colour are aligned across a diagonal

<img src="./Images/GameScreenshots/win_in_diagonal.png" height="200">

* All the moves on the board have been taken and the 
game is a draw