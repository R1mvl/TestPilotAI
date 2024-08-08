import numpy as np
from src.webexplor.preprocessing import Graph

class Curiosity:
    """
    Curiosity class that calculates the curiosity of the agent and updates the Q values, 
    this class is used by the agent to take actions based on the curiosity

    Attributes:
        N (Dict): Dictionary of N values {(S_p, A, S): N}
        Q (Dict): Dictionary of Q values {(S_p, A): Q}
        lambda_discount (float): Lambda discount value
        tau (int): Tau value

    Methods:
        curiosity(S_p, A, S): Curiosity function that returns the reward for the given action
        updateQ(S_p, A, S): Update the Q value for the given state and action
        gumbel_softmax(S, actions): Gumbel softmax function that returns the action to
    """

    def __init__(self):
        """
        Initializes the Curiosity class with the N and Q dictionaries, lambda discount value, and tau value
        """

        self.N = {}
        self.Q = {}

        self.lambda_discount = 0.9
        self.tau = 1

    def curiosity(self, S_p : Graph, A : Graph, S : Graph):
        """
        Curiosity function that returns the reward for the given action

        Args:
            S_p (State prime): previous state
            A (Action): Action taken
            S (State): Current state
        """

        if (S_p.state, A.action["locator"], S.state) not in self.N:
            self.N[(S_p.state, A.action["locator"], S.state)] = 1
        
        res = 1 / np.sqrt(self.N[(S_p.state, A.action["locator"], S.state)])

        return res

    def updateQ(self, S_p : Graph, A : Graph, S : Graph):
        """
        Update the Q value for the given state and action

        Args:
            S_p (State prime): previous state
            A (Action): Action taken
            S (State): Current state
        """

        max_Q_s = max(self.Q.get((S_p.state, A_p.action["locator"]), 0) for A_p in S_p.next)    
        reward = self.curiosity(S_p, A, S)
        
        self.Q[(S_p.state, A.action["locator"])] = reward + max_Q_s * self.lambda_discount

    def gumbel_softmax(self, S : Graph, actions : list):
        """
        Gumbel softmax function that returns the action to take, 
        using the gumbel softmax distribution to choose the action and Q values to calculate the probabilities

        Args:
            S (State): Current state
            actions (List[Action]): List of actions to choose from

        Returns:
            Action: Action to take
        """

        gumbel_values = np.random.gumbel(size=len(actions))
        q_values = []
        for action in actions:
            q_values.append(self.Q.get((S.state, action.action["locator"]), 0))

        q_values = np.array(q_values)
        
        logits = (q_values + gumbel_values) / self.tau
        probs = np.exp(logits) / np.sum(np.exp(logits))
        
        return np.random.choice(actions, p=probs)