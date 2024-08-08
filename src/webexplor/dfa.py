import collections
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import time

from src.webexplor.preprocessing import Graph

class DFA:
    """
    DFA class that represents the Deterministic Finite Automaton of the agent

    Attributes:
        dfa (list): List of states and curiosities
        count (int): Number of states in the DFA by the agent

    Methods:
        updateDFA(state): Update the DFA with the new state and curiosity
        checkDFA(state): Check if the state is already in the DFA
        getHighestCuriosity(): Get the page that give the highest curiosity
        SearchBestPath(root, state): Breadth First Search to find the shortest path from the root to a given state
        executePath(driver, path): Execute a path of actions
    """
    
    def __init__(self, max_states : int):
        """
        Initialize the DFA
        """

        self.dfa = []
        self.count = 0
        self.max_states = max_states

    def updateDFA(self, state : Graph):
        """
        Update the DFA with the new state and curiosity

        Args:
            state (Graph): The state to add to the DFA
        """


        for element in self.dfa:
            if element[0] == state:
                element[1] += 1
                self.count += 1
                print("Update DFA : ", state, "FOUND")
                return

        print("Update DFA : ", state, "NOT FOUND")
        self.dfa.append([state, 1])
        self.count = 0

    def checkDFA(self):
        """
        Check if we need too execute the DFA process, if we didn't find a new state since the last max_states states

        Args:
            None

        Returns:
            bool: True if the state is in the DFA and the counter is greater than the max_states, False otherwise
        """

        print("Count : ", self.count)

        if self.count >= self.max_states:
            self.count = 0
            return True

        return False
    
    def getHighestCuriosity(self):
        """
        Get the page that give the highest curiosity

        Returns:
            str: The page that give the highest curiosity
        """

        max_curiosity = 1000000
        max_state = None

        for element in self.dfa:
            state = element[0]
            curiosity = element[1]

            if curiosity < max_curiosity:
                max_curiosity = curiosity
                max_state = state

        return max_state

    def SearchBestPath(self, start : Graph, end : Graph):
        """
        Breadth First Search to find the shortest path from the root to a given state

        Args:
            start (Graph): The root of the graph
            end (Graph): The state to find

        Returns:
            list: The shortest path from the root to the state
        """

        visited = set()
        queue = collections.deque([(start, [start])])

        while queue:
            node, path = queue.popleft()

            if node is None:
                queue.append((None, path))
                continue

            visited.add(node)

            if node.state == end.state:
                return path

            for n in node.next:
                if n not in visited:
                    queue.append((n, path + [n]))

        return None
    
    def executePath(self, driver : WebDriver, path : list):
        """
        Execute a path of actions

        Args:
            driver (WebDriver): The WebDriver
            path (list): The path to execute
        """

        driver.get(path[0].state)

        for p in path:
            print("Execute : ", p)
            if p.type == 'action':
                if p.action["tag"] == 'input':
                    element = driver.find_element(By.XPATH, p.action["locator"])
                    element.send_keys(p.action["process"])
                else:
                    element = driver.find_element(By.XPATH, p.action["locator"])
                    element.click()
            elif p.type == 'state':
                if p.state != driver.current_url:
                    print("Error DFA : state not matching")

            time.sleep(1)
        
        time.sleep(5)
        if path[-1].state != driver.current_url:
            print("Error DFA : state not matching")

    