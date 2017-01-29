# Test Results
This file contains the console print outs of the simulators current supported. (dev branch of v1.1)
THe sub-heading should refer to the simulator used, followed by their results. These results were collected to
allow comparison between current and future work, as well as between the available simulators.

## Coordinator
_7 Servants_
```
Set up a game between Cheese Bot, Furniture Bot, and Dev Bot with the standard deck, and starting state.
Creating a 1000 game simulation...
Simulation took 14.061828136444092 seconds
Simulation Results:
	Total Games: 994
	Avg. Turns per game: 18.016096579476862
	Percentages:
		 Furniture Bot: 1.5090543259557343%
		 Cheese Bot: 48.89336016096579%
		 Dev Bot: 49.59758551307847%
	 Overall winner: Dev Bot with a percentage of 49.59758551307847
```

## Batch Simulator
_With 5 Workers_
```
Set up a game between Cheese Bot, Furniture Bot, and Dev Bot with the standard deck, and starting state.
Creating a 1000 game simulation...
Simulation took 150.60899376869202 seconds
Simulation Results:
	Total Games: 1000
	Avg. Turns per game: 18.047
	Percentages: 
		 Dev Bot: 47.8%
		 Furniture Bot: 1.7999999999999998%
		 Cheese Bot: 50.4%
	 Overall winner: Cheese Bot with a percentage of 50.4
```

_With 7 Workers_
```
Set up a game between Cheese Bot, Furniture Bot, and Dev Bot with the standard deck, and starting state.
Creating a 1000 game simulation...
Simulation took 150.24892926216125 seconds
Simulation Results:
	Total Games: 994
	Avg. Turns per game: 18.120724346076457
	Percentages: 
		 Cheese Bot: 47.88732394366197%
		 Dev Bot: 50.40241448692153%
		 Furniture Bot: 1.710261569416499%
	 Overall winner: Dev Bot with a percentage of 50.40241448692153
```
_Comments_
The Batch simulator may have been implemented poorly, as it appears to only run on a single core.
May drop this during next release.

## Simulator
```
Set up a game between Cheese Bot, Furniture Bot, and Dev Bot with the standard deck, and starting state.
Creating a 1000 game simulation...
Simulation took 81.92231297492981 seconds
Simulation Results:
	Total Games: 1000
	Avg. Turns per game: 18.104
	Percentages: 
		 Dev Bot: 50.0%
		 Cheese Bot: 48.4%
		 Furniture Bot: 1.6%
	 Overall winner: Dev Bot with a percentage of 50.0
```
