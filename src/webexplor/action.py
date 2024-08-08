from transformers import AutoModelForCausalLM, AutoTokenizer
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from src.webexplor.preprocessing import getStateNode, Graph

class Action:
    """
    Action class that takes the action to be performed and processes it

    Attributes:
        patternList (List[Pattern]): List of patterns to match the action
        model (AutoModelForCausalLM): Model to generate the input text
        tokenizer (AutoTokenizer): Tokenizer to tokenize the input text

    Methods:
        getInputText(inputString): Get the input text from the model
        getInputPattern(locator): Get the input pattern from the pattern list
        processAction(driver, current): Process the action to be performed
        
    """

    def __init__(self, patternList : list):
        """
        Initializes the Action class with the pattern list, model, and tokenizer

        Args:
            patternList (List[Pattern]): List of patterns to match the action, Pattern is a dictionary with keys 'type', 'XPath', 'value'
        """
        self.model = AutoModelForCausalLM.from_pretrained(
            "Qwen/Qwen2-1.5B-Instruct",
            torch_dtype="auto",
            device_map="auto"
        )

        self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-1.5B-Instruct")
        self.patternList = patternList

    def getInputText(self, inputString : str):
        """
        Get the input text from the model

        Args:
            inputString (str): Input string to generate the text

        Returns:
            str: Generated text
        """

        print("Qwen/Qwen2-1.5B-Instruct with Input ===>", inputString)

        messages = [
            {"role": "user", "content": "Give me an example for my input, give me only the answer " + inputString + " :"},
        ]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt")

        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=30
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        response = response.split(":")
        if len(response) > 1:
            response = response[1].strip()
        else:
            response = response[0].strip()

        print("Qwen/Qwen2-1.5B-Instruct generate ===>", response)

        return response
    
    def getInputPattern(self, locator : str):
        """
        Get the input pattern from the pattern list, if the locator matches the pattern else return None

        Args:
            locator (str): Locator to match the pattern

        Returns:
            Pattern: Pattern matched
        """

        for pattern in self.patternList:
            if pattern['XPath'] == locator:
                print("Pattern Matched ===>", pattern)
                return pattern
            
        print("Pattern Not Matched")
        return None

    def processAction(self, driver : webdriver, current : Graph):
        """
        Process the action to be performed

        Args:
            driver: Selenium WebDriver
            current (Graph): Current node

        Returns:
            Graph: New state node
        """

        action = current.action
        
        if action['type'] == 'text':
            placeholder = action['placeholder'] if action['placeholder'] else action['id']
            text = self.getInputText(placeholder) if not self.getInputPattern(action['locator']) else placeholder

            action['process'] = text
            driver.find_element(By.XPATH, action['locator']).send_keys(text)
        else:
            driver.find_element(By.XPATH, action['locator']).click()
            action['process'] = "Click"

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        except:
            return None
        
        state, _ = getStateNode(driver, current, [])

        return state
