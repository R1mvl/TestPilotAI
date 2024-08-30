from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Login:
    """
    Login class that detects the login page and executes the login

    Attributes:
        url (str): URL of the login page
        patternList (List[Pattern]): List of patterns to match the action

    Methods:
        detectloginPage(driver): Detect the login page
        executeLogin(driver): Execute the login
    """

    def __init__(self, url, patternList):
        """
        Initializes the Login class with the URL and pattern list

        Args:
            url (str): URL of the login page
            patternList (List[Pattern]): List of patterns to match the action, Pattern is a dictionary with keys 'type', 'XPath', 'value'
        """

        self.url = url
        self.patternList = patternList

    def detectloginPage(self, driver):
        """
        Detect the login page

        Args:
            driver: Selenium WebDriver

        Returns:
            True if the login page has been detected, False otherwise
        """
        
        if self.url == driver.current_url:
            return True
        
        return False
    
    def executeLogin(self, driver):
        """
        Execute the login pattern by entering the values in the input fields and clicking the button

        Args:
            driver: Selenium WebDriver
        """
        
        for pattern in self.patternList:
            if pattern["type"] == "input":
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, pattern["XPath"]))).send_keys(pattern["value"])
            elif pattern["type"] == "click":
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, pattern["XPath"]))).click()