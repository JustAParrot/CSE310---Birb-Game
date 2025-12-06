Flappy Birb (Duck) – A Python Arcade Game

A tiny duck, a giant dream, and way too many pipes.

Welcome to Flappy Duck, a playful clone of the classic mobile game — created using the Python Arcade library.
This project focuses on user input, animations, collision mechanics, sound effects, and classic 2D game loops.

- How It Works

The game opens with a simple start screen.
Pressing SPACE launches the duck into the air.
The bird constantly falls, so careful timing is needed to navigate between randomly generated pipe gaps.
If the duck hits a pipe or the ground... game over D:
Press SPACE again to restart your attempt!

- Game Features
    - Graphics
    - Custom bird sprite
    - Top & bottom pipe sprites
    - Scrolling environment
    - Smooth movement & collisions
    - Clean background with ground & sky

    User Input
    - SPACE makes the bird flap
    - SPACE also starts or restarts the game

    Moving Objects
    - The bird has gravity and velocity
    - Pipes scroll from right to left
    - Pipes reset with random heights
    - Score increases for each passed pipe

    Sound Effects (Additional Requirement Completed)
    - Flap sound
    - Point sound
    - Hit sound

- Technology Used
    - Python 3.12
    - Arcade Library
    - Pyglet (via Arcade)
    - Visual Studio Code

To install Arcade, run:
    
    pip install arcade

- How to Run the Game

    - Make sure your folder looks like this:

    CSE310---Birb-Game/
    │ main.py
    │ README.txt
    │ sprites
        │ bird.png
        │ pipe_top.png
        │ pipe_bottom.png
    │ sounds
        │ flap.wav
        │ hit.wav
        │ point.wav


    - Then run:

    python main.py

    Game starts instantly.
    Press SPACE to begin!

- Final Notes

This project was created to practice game loops, physics, collision detection, sprite handling, and event-based 
input using the Arcade framework. It was also a fun chance to bring a tiny duck to life and make it suffer 
through pipes (sorry birb).

THX for reading! :D