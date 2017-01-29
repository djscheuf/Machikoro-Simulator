# Machikoro Simulator
This is a relatively simple simulator for the board game Machikoro.
A single turn of the game involves the following:
* Each player rolls 1 or 2 dice, depending on the improvements they have
* Each player can earn money base on the roll:
    * Steal it from the current player
    * Earn it from _'natural features'_
    * Earn it from their factories
* The goal of the game is to purchase all the major improvements

## Phase 1 - Base
Phase 1 involves just getting the basic game simulation working.
This includes basic AI, and of course logging the actions during the game
Preference is for a fluent API.

Note: Phase 1 is complete in Master

## Phase 2 - Simulation
After the base game can be simulated, it comes time to run more games.
This will provide information on effective strategies.
A basic simulator will be needed, and some re-factoring of the game, and it's logging.
It will also likely involve running multiple games in parallel. And some appropriate
logging for the simulation.
[\] Basic Simulator
[ ] Parallel Games

##Beyond
Additional features may eventually include:
* User interaction, so users can play against AI
* _Genetic Evolution of AIs_
* Alternative AI patterns, rather than the dummy currently in-place
* Alternative Decks
* Support for expansion packs
* Possible a UI to interact with the simulators/game?




