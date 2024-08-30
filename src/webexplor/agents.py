from src.webexplor.preprocessing import getStateNode, getActionsNode, Graph, getRoot
from src.webexplor.goalErrorDetection import newWindowDetection, goalDetection, errorDetection, pageNotLoaded, resetGoalError
from src.webexplor.action import Action
from src.webexplor.curiosity import Curiosity
from src.webexplor.dfa import DFA
from selenium import webdriver


def curiosityAgent(driver : webdriver, current : Graph, website : dict, Action : Action, Curiosity : Curiosity):
    """
    Curiosity agent that takes actions based on the curiosity of the agent and updates the Q values,
    and detects if a new window is opened, goal is reached, error has occurred, or page is not loaded

    Args:
        driver: Selenium WebDriver
        current (Graph): Current state node
        N (Dict): Dictionary of N values
        Q (Dict): Dictionary of Q values
        Errors (List): List of error worklfow
        Goals (List): List of goal worklfow
        workflow (List): List of nodes of the current workflow
        Action (Action): Action class

    Returns:
        current (Graph): Current state node
    """

    initial_windows = driver.window_handles
    
    # get the current state and actions
    S, current = getStateNode(driver, current, website["workflow"])
    actions = getActionsNode(driver, current)

    if len(actions) == 0:
        S = Graph('state', previous=current, state="Error : No actions", status='Error', reason="No actions available")
        website["nbError"] += 1
        current, website["workflow"], website["errorList"] = resetGoalError(driver=driver, S=S, current=current, workflow=website["workflow"], list=website["errorList"])

        return current

    # take an action based on the curiosity
    A = Curiosity.gumbel_softmax(S, actions)

    # perform the action
    website["workflow"].append(A)
    current = A
    S_p = S
    S = Action.processAction(driver, current)

    # check if a new window is opened
    if newWindowDetection(driver, initial_windows, website):
        S = Graph('state', previous=current, state=website["reason"], status='Error', reason="New window\n" + website["reason"])
        website["nbError"] += 1
        Curiosity.Q[(S_p.state, A.action["locator"])] = -1000
        current, website["workflow"], website["errorList"] = resetGoalError(driver=driver, S=S, current=current, workflow=website["workflow"], list=website["errorList"])

    elif goalDetection(driver, website):
        S.status = 'Goal'
        S.reason = website["reason"]
        website["nbGoal"] += 1
        current, website["workflow"], website["goalList"] = resetGoalError(driver=driver, S=S, current=current, workflow=website["workflow"], list=website["goalList"])

    elif errorDetection(driver, website):
        S = Graph('state', previous=current, state="Error : error in the console", status='Error', reason=website["reason"])
        website["nbError"] += 1
        current, website["workflow"], website["errorList"] = resetGoalError(driver=driver, S=S, current=current, workflow=website["workflow"], list=website["errorList"])

    elif pageNotLoaded(driver, S, website):
        S = Graph('state', previous=current, state="Error : page not loaded", status='Error', reason=website["reason"])
        website["nbError"] += 1
        current, website["workflow"], website["errorList"] = resetGoalError(driver=driver, S=S, current=current, workflow=website["workflow"], list=website["errorList"])

    else:
        Curiosity.updateQ(S_p, A, S)
        Curiosity.N[(S_p.state, A.action["locator"], S.state)] += 1
        current = S

    return current

def DfaAgent(driver : webdriver, current : Graph, website : dict, Action : Action, Curiosity : Curiosity, DFA : DFA):
    """
    DFA agent that takes actions based on the curiosity of the agent and updates the Q values,
    and detects if a new window is opened, goal is reached, error has occurred, or page is not loaded.
    The DFA agent uses the DFA to resolve the randomness of the curiosity agent.

    Args:
        driver: Selenium WebDriver
        current (Graph): Current state node
        N (Dict): Dictionary of N values
        Q (Dict): Dictionary of Q values
        Errors (List): List of error worklfow
        Goals (List): List of goal worklfow
        workflow (List): List of nodes of the current workflow
        Action (Action): Action class

    Returns:
        current (Graph): Current state node
    """

    initial_windows = driver.window_handles
    
    # get the current state and actions
    S, current = getStateNode(driver, current, website["workflow"])
    actions = getActionsNode(driver, current)

    if len(actions) == 0:
        S = Graph('state', previous=current, state="Error : No actions", status='Error', reason="No actions available")
        website["nbError"] += 1
        current, website["workflow"], website["errorList"] = resetGoalError(driver=driver, S=S, current=current, workflow=website["workflow"], list=website["errorList"])

        return current

    # take an action based on the curiosity
    A = Curiosity.gumbel_softmax(S, actions)

    # perform the action
    website["workflow"].append(A)
    current = A
    S_p = S
    S = Action.processAction(driver, current)


    # check if a new window is opened
    if newWindowDetection(driver, initial_windows, website):
        S = Graph('state', previous=current, state="Error : new window opened", status='Error', reason=website["reason"])
        website["nbError"] += 1
        Curiosity.Q[(S_p.state, A.action["locator"])] = -1000
        current, website["workflow"], website["errorList"] = resetGoalError(driver=driver, S=S, current=current, workflow=website["workflow"], list=website["errorList"])

    elif goalDetection(driver, website):
        S = Graph('state', previous=current, state="Goal reached", status='Goal', reason=website["reason"])
        website["nbGoal"] += 1
        current, website["workflow"], website["goalList"] = resetGoalError(driver=driver, S=S, current=current, workflow=website["workflow"], list=website["goalList"])

    elif errorDetection(driver, website):
        S = Graph('state', previous=current, state="Error : error in the console", status='Error', reason=website["reason"])
        website["nbError"] += 1
        current, website["workflow"], website["errorList"] = resetGoalError(driver=driver, S=S, current=current, workflow=website["workflow"], list=website["errorList"])

    elif pageNotLoaded(driver, S, website):
        S = Graph('state', previous=current, state="Error : page not loaded", status='Error', reason=website["reason"])
        website["nbError"] += 1
        current, website["workflow"], website["errorList"] = resetGoalError(driver=driver, S=S, current=current, workflow=website["workflow"], list=website["errorList"])

    else:
        if DFA.checkDFA():
            stateHighestCuriosity = DFA.getHighestCuriosity()
            print("State with highest curiosity : ", stateHighestCuriosity)
            path = DFA.SearchBestPath(getRoot(current), stateHighestCuriosity)
            print("Path : ")
            for p in path:
                print(p)
                
            DFA.executePath(driver, path)

            website["workflow"] = path
            current = path[-1]
            DFA.updateDFA(current)

            print("DFA path executed")
            print("Current : ", current, "action : ", current.action, "state : ", current.state)
            print("==============================")
        else:
            DFA.updateDFA(S)
            Curiosity.updateQ(S_p, A, S)
            Curiosity.N[(S_p.state, A.action["locator"], S.state)] += 1
            current = S

    return current