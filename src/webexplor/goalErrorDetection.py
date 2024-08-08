from src.webexplor.preprocessing import getRoot

def newWindowDetection(driver, initial_windows, website):
    """
    Detects if a new window has been opened and closes it

    Args:
        driver: Selenium WebDriver
        initial_windows: List of initial windows
        website: Website object

    Returns:
        True if a new window has been opened and closed, False otherwise
    """

    if len(driver.window_handles) != len(initial_windows):

        for window in driver.window_handles:
            if window not in initial_windows:
                driver.switch_to.window(window)
                website["reason"] = "New window\n" + driver.current_url
                driver.close()

        driver.switch_to.window(initial_windows[0])

        return True
    
    return False

def goalDetection(driver, website):
    """
    Detects if the goal has been reached

    Args:
        driver: Selenium WebDriver
        website: Website object

    Returns:
        True if the goal has been reached, False otherwise
    """

    goal = website["targetURL"]

    if not goal:
        return False

    if goal == driver.current_url:
        website["reason"] = "Goal with the target URL reached\n" + goal
        return True

    return False

def errorDetection(driver, website):
    """
    Detects if an error has occurred in the console

    Args:
        driver: Selenium WebDriver
        website: Website object

    Returns:
        True if an error has occurred, False otherwise
    """

    error = driver.execute_script('return document.querySelector(".error")')

    if error:
        website["reason"] = "Error in the console\n" + error.text
        return True
    
    return False

def pageNotLoaded(driver, S, website):
    """
    Detects if the page has not loaded

    Args:
        driver: Selenium WebDriver
        S: State
        website: Website object

    Returns:
        True if the page has not loaded, False otherwise
    """

    if not S:
        website["reason"] = "Page not loaded \n" + driver.current_url
        return True
    
    return False

def resetGoalError(driver, S, current, workflow, list):
    """
    Resets the state of the page to the root state, save the workflow in the list and start a new one

    Args:
        driver: Selenium WebDriver
        S: State
        current: Current state
        workflow: List of states
        list: List of workflows

    Returns:
        current: Current state
        workflow: List of states
        list: List of workflows
    """

    workflow.append(S)
    current = getRoot(current)
    driver.get(current.state)
    list.append(workflow)
    workflow = []

    return current, workflow, list