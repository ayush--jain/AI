## REINFORCEMENT LEARNING : <br \>

###Instructions to run:

This project requires **Python 2.7** with the [pygame](https://www.pygame.org/wiki/GettingStarted
) library installed. When in the directory, run it as: python smartcab/agent.py

###Q-learning-

A basic self driving car has been implemented using pygame for visualization.

smartcab operates in an idealized grid-like city, with roads going North-South and East-West. Other vehicles may be present on the roads, but no pedestrians. There is a traffic light at each intersection that can be in one of two states: North-South open or East-West open. It assumes the road network to be a torus.

US right-of-way rules apply: On a green light, you can turn left only if there is no oncoming traffic at the intersection coming straight. On a red light, you can turn right if there is no oncoming traffic turning left or traffic from the left going straight.

100 trials have been used for training the smartcab and other optimizations to the algo has been implemented to achieve the optimal policy.
