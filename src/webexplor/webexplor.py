from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import threading
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from src.webexplor.action import Action
from src.webexplor.curiosity import Curiosity
from src.webexplor.dfa import DFA
from src.webexplor.login import Login
from src.webexplor.agents import curiosityAgent, DfaAgent
from src.webexplor.preprocessing import printGraph, getRoot

def runAgent(website, agent="Curiosity"):

    currentTime = time.time()
    action = Action(website["inputPatterns"])
    login = Login(website["loginURL"], website["loginPatterns"])
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.binary_location = "/usr/bin/google-chrome"

    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    current = None
    N = None

    while website["repeat"] < website["maxRepeat"]:

        curiosity = Curiosity()
        if N is not None:
            curiosity.N = N

        dfa = DFA(max_states=5)

        website["time"] = 0
        website["workflow"] = []
        driver.get(website["websiteURL"])


        if current is not None:
            current = getRoot(current)
            website["workflow"] = []

        while website["time"] < website["maxTime"]:
            print("THREAD RUNNING TIME : ", website["time"] , "/" , website["maxTime"])

            if login.detectloginPage(driver):
                login.executeLogin(driver)
                time.sleep(1)

            #current = curiosityAgent(driver, current, website, action, curiosity)
            current = DfaAgent(driver, current, website, action, curiosity, dfa)

            while time.time() - currentTime > 60:
                website["time"] += 1
                currentTime += 60

            time.sleep(1)

        website["repeat"] += 1
        N = curiosity.N
        print("REPEAT : ", website["repeat"] , "/" , website["maxRepeat"])


    driver.quit()

    G_final = getRoot(current).drawGraph(nx.DiGraph(), allNodes=False)
    website["map"] = G_final

    return website

def webExplor(website, agent="Curiosity"): 

    thread = threading.Thread(target=runAgent, args=(website, agent))
    thread.start()

    thread.join()


    print("THREAD FINISHED ...")

    website["map"] = printGraph(website["map"])

    print("Map generated")

    return website