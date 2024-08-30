import requests
import uuid
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import networkx as nx
import asyncio

from src.api.generator import seleniumTestgenerator, playwrightPythonTestGenerator, playwrightTestGeneratorJavaScript, playwrightTestGeneratorJava, robotTestGenerator
from src.webexplor.webexplor import webExplor

websiteQueue = []
websiteInTest = None
websiteCompleted = []

def runWebTesting(data):
    global websiteQueue

    # try to request the website to know if it is valid
    try:
        print(data["websiteURL"])
        #r = requests.get(data["websiteURL"])
    except:
        return 400

    # change the data type
    data["maxRepeat"] = int(data["maxRepeat"])
    data["maxTime"] = int(data["maxTime"])
    data["id"] = str(uuid.uuid4())

    # Add the website to the queue
    websiteQueue.append(data)

    print(data)
    print("Len of websiteQueue", len(websiteQueue))
    print("websiteInTest", websiteInTest)
    print("websiteCompleted", websiteCompleted)

    return 200


def getTestElement(testElement):
    return {
        "id": testElement["id"],
        "websiteURL": testElement["websiteURL"],
        "repeat": testElement["repeat"],
        "maxRepeat": testElement["maxRepeat"],
        "time": testElement["time"],
        "maxTime": testElement["maxTime"],
        "nbGoal": testElement["nbGoal"],
        "nbError": testElement["nbError"],
    }

def getTests():
    if websiteInTest is None:
        testInProgress = None
    else:
        testInProgress = getTestElement(websiteInTest)

    testCompleted = []
    for website in websiteCompleted:
        testCompleted.append(getTestElement(website))

    return {
        "testInQueue": websiteQueue,
        "testInProgress": testInProgress,
        "testCompleted": testCompleted,
    }

def cancelTestQueue(id):
    global websiteQueue

    for i in range(len(websiteQueue)):
        if websiteQueue[i]["id"] == id:
            websiteQueue.pop(i)
            return 200

    return 404

def getPlotResult(nodeList):
    G = nx.DiGraph()
    res = {"id": str(uuid.uuid4()), "nodes": [], "image": None, "reason": None}

    for j in range(len(nodeList)):
        node = nodeList[j]

        if node.reason is not None:
            res["reason"] = node.reason

        node = {
            "id": node.id,
            "state": node.state if node.type == "state" or node.type == "root" else node.action["locator"],
            "type": node.type,
            "status": node.status,
            "process": node.action["process"] if node.type == "action" and node.action["type"] == "text" else None,
        }

        res["nodes"].append(node)

        color = None
        if node["type"] == "root":
            color = "yellow"
        elif node["type"] == "action":
            color = "blue"
        elif node["status"] == "Error":
            color = "red"
        elif node["status"] == "Goal":
            color = "cyan"
        else:
            color = "green"

        label = node["state"]

        if node["type"] == "state" and node["status"] == "Error":
            label = "Error"
        elif node["type"] == "state" and node["status"] == "Goal":
            label = "Goal"

        G.add_node(node["id"], color=color, label=label)
        print(node["id"], node["state"], node["type"], node["status"])
        if node["type"] != "root":
            G.add_edge(nodeList[j - 1].id, node["id"])

    # Define custom horizontal layout
    pos = {node: (i, 0) for i, node in enumerate(G.nodes())}

    # Plot the graph
    plt.figure(figsize=(20, 3))
    nx.draw(
        G,
        pos,
        node_color=[G.nodes[node]["color"] for node in G.nodes()],
        with_labels=False,
        node_size=2000,
        font_size=10,
        arrows=True,
    )
    for node, (x, y) in pos.items():
        plt.text(
            x,
            y,
            G.nodes[node]["label"],
            horizontalalignment="center",
            verticalalignment="center",
            rotation=30,
            fontsize=10,
            color="black",
            bbox=dict(facecolor="white", alpha=0.5, edgecolor="none"),
        )

    plt.axis("off")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    res["image"] = base64.b64encode(buf.read()).decode("utf-8")

    plt.close()

    return res

def getResult(id):

    for website in websiteCompleted:
        if website["id"] == id:

            if 'errorNodeList' not in website or 'goalNodeList' not in website:
                website["errorNodeList"] = []
                website["goalNodeList"] = []

                for i in range(len(website["errorList"])):
                    res = getPlotResult(website["errorList"][i])
                    website["errorNodeList"].append(res)

                for i in range(len(website["goalList"])):
                    res = getPlotResult(website["goalList"][i])
                    website["goalNodeList"].append(res)

            return {
                "websiteURL": website["websiteURL"],
                "id": website["id"],
                "maxRepeat": website["maxRepeat"],
                "time": website["time"],
                "maxTime": website["maxTime"],
                "websiteMap": website["map"],
                "nbGoal": website["nbGoal"],
                "nbError": website["nbError"],
                "errorNodeList": website["errorNodeList"],
                "goalNodeList": website["goalNodeList"],
            }

    return None

def generateTest(testId, nodeId, language):
    print("idTest", testId)
    print("idNode", nodeId)
    print("language", language)
    for website in websiteCompleted:
        if website["id"] == testId:
            for error in website["errorNodeList"]:
                print("error", error['id'])
                if error["id"] == nodeId:
                    if language == "playwrightPython":
                        return playwrightPythonTestGenerator(website, error)
                    elif language == "playwrightJavaScript":
                        return playwrightTestGeneratorJavaScript(website, error)
                    elif language == "playwrightJava":
                        return playwrightTestGeneratorJava(website, error)
                    elif language == "selenium":
                        return seleniumTestgenerator(website, error)
                    elif language == "robot":
                        return robotTestGenerator(website, error)
                    

            for goal in website["goalNodeList"]:
                if goal["id"] == nodeId:
                    print("goal", goal['id'])
                    if language == "playwrightPython":
                        return playwrightPythonTestGenerator(website, goal)
                    elif language == "playwrightJavaScript":
                        return playwrightTestGeneratorJavaScript(website, goal)
                    elif language == "playwrightJava":
                        return playwrightTestGeneratorJava(website, goal)
                    elif language == "selenium":
                        return seleniumTestgenerator(website, error)
                    elif language == "robot":
                        return robotTestGenerator(website, error)

async def runTest():
    global websiteInTest, websiteCompleted

    websiteInTest["repeat"] = 0
    websiteInTest["time"] = 0
    websiteInTest["nbGoal"] = 0
    websiteInTest["nbError"] = 0
    websiteInTest["errorList"] = []
    websiteInTest["goalList"] = []

    webExplor(websiteInTest)

    websiteCompleted.append(websiteInTest)
    websiteInTest = None


async def process_queue():
    global websiteInTest, websiteQueue, websiteCompleted

    while True:

        if len(websiteQueue) > 0 and websiteInTest is None:
            websiteInTest = websiteQueue.pop(0)

            # Simulate a test
            await runTest()
        else:
            await asyncio.sleep(1)
