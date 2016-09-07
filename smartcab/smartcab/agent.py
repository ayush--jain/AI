import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        #super() is used for inherinting class Agent from environment.py
        self.color = 'black'  # override color

        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        
        # TODO: Initialize any additional variables here
        self.action = None
        self.next_waypoint_new = None
        self.next_state = None
        self.e = 0.1  #initialize epsilon for epsilon greedy
        self.temp = 1.0

        #initialize qtable to default value (0 for int)
        from collections import defaultdict
        self.qtable = defaultdict(lambda:2)  #Initialize Q(s, a)

    #new trial
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.action = None  #NOTE: check if this should be randomized
        self.state = None
        self.next_state = None

        
    # helper func for updating q table
    def argmax(self, current_state):
        '''selects the best action from the state
            using policy derived from the Q-table'''
        best_action= random.choice(Environment.valid_actions) #initialize the best action to a random value
        qval = self.qtable[(current_state, best_action)]      #intialize qval which will store the highest Q-value for the next (state, action)
        for (state,action) in self.qtable:                         # for all Q(s,a) pairs in qtable, if any have a greater Q value than current for same state:
            if state == current_state and self.qtable[(state,action)] > qval:
                best_action = action                          # update action
                qval = self.qtable[(state,action)]            # update qvalue
        return best_action

    #update at every step till we reach destination or deadline
    def update(self, t): #t is the no of step at which we are
        ###########################
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)  #check if we can move forward i.e. green light and  no oncoming traffic - gets dic tnot a boolean
        deadline = self.env.get_deadline(self) #gets deadline from Environment which is (dist b/w start-dest.) *5
        ############################
        
        # Update state
        self.state = (('light',inputs['light']),('oncoming', inputs['oncoming']), ('left', inputs['left']), ('right', inputs['right']), 
                        self.next_waypoint)

        ############################
        # Select action according to your policy
        
        #update epsilon
        self.e = 1.0/self.temp
        self.temp += 0.1

        #epsilon greedy
        #if epsilon is low (first 50 steps or so) 
        if self.e > 0.016 or random.random() < self.e: # for later steps select with epsilon probability (if a random no. b/w 0 & 1 trumps epsilon)
            self.action = random.choice(Environment.valid_actions)

        else:
            self.action = self.argmax(self.state)
        ##############################

        # Execute action and get reward
        reward = self.env.act(self, self.action)

        ##############################

        # TODO: Learn policy based on state, action, reward
        alpha = 0.1  #how much data is being overriden in each cycle- learning rate
        gamma = 0.1  #how much future reward is valued(closer to 0 means more immediate reward is considered)- discount factor    

        #get next set of state action paur
        self.next_waypoint_new = self.planner.next_waypoint()
        inputs_new = self.env.sense(self)

        self.next_state = (('light',inputs_new['light']),('oncoming', inputs_new['oncoming']), ('left', inputs_new['left']), ('right', inputs_new['right']), 
                            self.next_waypoint_new)
        next_action = self.argmax(self.next_state)

        #Q (s, a) <-- Q(s, a) + alpha [r + gamma* max(a')Q(s', a') - Q(s, a)]
        self.qtable[(self.state,self.action)] += alpha * (reward + gamma* self.qtable[(self.next_state, next_action)] - self.qtable[(self.state, self.action)] )

        
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, self.action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials

if __name__ == '__main__':
    run()
