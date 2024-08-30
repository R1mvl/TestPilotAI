import matplotlib.pyplot as plt
import collections
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from networkx.drawing.layout import spring_layout
import matplotlib.patches as mpatches
import base64
from io import BytesIO 
from selenium import webdriver

def getDom(driver : webdriver) -> list:
    """
    Get the DOM of the current page

    Args:
        driver: Selenium WebDriver object

    Returns:
        dom: DOM of the current page
    """

    dom_elements = driver.execute_script('''
        var elements = document.getElementsByTagName('*');
        var tags = [];
        for (var i = 0; i < elements.length; i++) {
            tags.push(elements[i].tagName.toLowerCase());
        }
        return tags;
    ''')
    return dom_elements

def getActions(driver : webdriver) -> list:
    """
    Get the interactable elements on the current page

    Args:
        driver: Selenium WebDriver object

    Returns:
        actions: List of interactable elements 
        {
            type: type of the element,
            tag: tag of the element,
            id: id of the element,
            class: class of the element,
            locator: xpath of the element,
        }
    """

    script = """
    function getXPathForElement(element) {
        var xpath = '';
        while (element && element.nodeType === Node.ELEMENT_NODE) {
            var id = element.getAttribute('id');
            if (id) {
                xpath = '//*[@id="' + id + '"]' + xpath;
                break;
            } else {
                var index = 1;
                var sibling = element.previousSibling;
                while (sibling) {
                    if (sibling.nodeType === Node.ELEMENT_NODE && sibling.nodeName === element.nodeName) {
                        index++;
                    }
                    sibling = sibling.previousSibling;
                }
                var tagName = element.nodeName.toLowerCase();
                xpath = '/' + tagName + '[' + index + ']' + xpath;
                element = element.parentNode;
            }
        }
        return xpath;
    }

    function isElementInteractable(element) {
        var style = window.getComputedStyle(element);
        var isVisible = style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';
        var isEnabled = !element.disabled && !element.hasAttribute('disabled');
        var hasSize = element.offsetWidth > 0 && element.offsetHeight > 0;
        var isNotHidden = !element.hasAttribute('hidden');
        return isVisible && isEnabled && hasSize && isNotHidden;
    }

    function isElementAndParentsVisible(element) {
        while (element) {
            if (!isElementInteractable(element)) {
                return false;
            }
            element = element.parentElement;
        }
        return true;
    }

    function getInteractableElements() {
        var elements = document.getElementsByTagName('*');
        var tags = [];
        for (var i = 0; i < elements.length; i++) {
            var element = elements[i];
            var tag = element.tagName.toLowerCase();
            if (tag === 'input' || tag === 'textarea' || tag === 'select' || tag === 'button' || tag === 'a' || tag === 'label') {
                if (isElementAndParentsVisible(element)) {
                    var type = element.type || '';
                    var id = element.id || '';
                    var className = element.className || '';
                    var locator = getXPathForElement(element);
                    var placeholder = element.placeholder || '';

                    tags.push({
                        type: type,
                        tag: tag,
                        id: id,
                        class: className,
                        locator: locator,
                        placeholder: placeholder,
                    });
                }
            }
        }
        return tags;
    }

    return getInteractableElements();
    """
    actions = driver.execute_script(script)
    return actions

def GestaltPatternMatching(s1 : str, s2 : str) -> float:
    """
    Calculate the similarity between two strings using Gestalt Pattern Matching

    Args:
        s1: First string
        s2: Second string

    Returns:
        float: Similarity between the two strings
    """

    length = len(s1) + len(s2)

    if not length:
        return 1.0

    intersect = collections.Counter(s1) & collections.Counter(s2)
    matches = sum(intersect.values())
    return 2.0 * matches / length

class Graph:
    """
    Graph class to represent the workflow of the web application

    Attributes:
        node_count: Number of nodes in the graph
        id: Unique ID of the node
        type: Type of the node, either action or state
        action: Action details if the node is an action
        state: State details if the node is a state
        dom: DOM of the state
        next: List of nodes that are reachable from the current node
        prev: List of nodes that can reach the current node
        status: Status of the node, either Success or Failure

    Methods:
        __init__: Initialize the Graph object
        __str__: Return the string representation of the node
        drawGraph: Draw the graph using NetworkX
    """

    node_count = 0
    
    def __init__(self, type : str, previous : 'Graph' = None, action : dict = None, state : str = None, dom : list = None, status : str = None, reason : str = None):
        """
        Initialize the Graph object

        Args:
            type: Type of the node, either action or state
            previous: Previous node in the graph
            action: Action details if the node is an action
            state: State details if the node is a state
            dom: DOM of the state if the node is a state
            status: Status of the node, either Success or Failure
        """

        self.id = Graph.node_count
        Graph.node_count += 1

        self.type = type                        # action or state
        self.action = action                    # action details
        self.state = state                      # state details
        self.dom = dom                          # DOM of the state
        self.next = []                          # list of nodes that are reachable from the current node
        self.prev = []                          # list of nodes that can reach the current node
        self.status = status if state else None # status of the node, either Success or Failure
        self.reason = reason                    # reason for the status only for Goal and Error

        if previous:
            previous.next.append(self)
            self.prev.append(previous)

    def __str__(self):
        """
        Return the string representation of the node

        Returns:
            str: String representation of the node
        """

        if self.type == 'action':
            res =  f'{self.action["locator"]}'
            return res
        else:
            res = f'{self.state}'
            return '"' + res + '"' 
 
    def drawGraph(self, G : nx.DiGraph, allNodes : bool = False) -> nx.DiGraph:
        """
        Draw the graph using NetworkX

        Args:
            G: NetworkX Graph object
            allNodes: Boolean to include all nodes in the graph

        Returns:
            G: NetworkX Graph object
        """

        if self.type == 'root':
            G.add_node(self.id, color='yellow', label=str(self))
        
        for node in self.next:
            color = None
            if node.type == "root":
                color = "yellow"
            elif node.type == "action":
                color = "blue"
            elif node.status == "Error":
                color = "red"
            elif node.status == "Goal":
                color = "cyan"
            else:
                color = "green"

            label = str(node) if node.type == 'state' and node.status == 'Success' else ""

            if allNodes:
                if node.id not in G.nodes:
                    G.add_node(node.id, color=color, label=label)
                    G.add_edge(self.id, node.id)
                    node.drawGraph(G, allNodes)
                else:
                    G.add_edge(self.id, node.id)
            
            elif len(node.next) > 0 or node.type == 'state':
                if node.id not in G.nodes:
                    G.add_node(node.id, color=color, label=label)
                    G.add_edge(self.id, node.id)
                    node.drawGraph(G, allNodes)
                else:
                    G.add_edge(self.id, node.id)

        return G
    
def printGraph(G: nx.DiGraph, size: tuple = (20, 20)) -> str:
    """
    Print the graph using NetworkX

    Args:
        G: NetworkX Graph object
        size: Size of the graph

    Returns:
        plot: plot encoded in base64
    """

    # Define custom tree layout
    pos = graphviz_layout(G, prog="twopi")
    #pos = spring_layout(G)

    plt.figure(figsize=size)
    nx.draw(G, pos, arrows=True, with_labels=True, node_color=[G.nodes[n]['color'] for n in G.nodes], labels=nx.get_node_attributes(G, 'label'))
    
    root_patch = mpatches.Patch(color='yellow', label='Root')
    error_patch = mpatches.Patch(color='red', label='Error')
    success_patch = mpatches.Patch(color='green', label='Success')
    action_patch = mpatches.Patch(color='blue', label='Action')
    goal_patch = mpatches.Patch(color='cyan', label='Goal')
    plt.legend(handles=[root_patch, error_patch, success_patch, action_patch, goal_patch], loc='upper left')


    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    plot = base64.b64encode(buf.getvalue()).decode('utf8')
    plt.close()

    return plot

def getStateSet(root : Graph) -> list:
    """
    Get the set of states in the graph

    Args:
        root: Root node of the graph

    Returns:
        res: List of states in the graph
    """

    visited = []
    res = []

    def getStateSetRec(node):
        if node.type == 'state' or node.type == 'root':
            res.append({'state': node.state, 'dom': node.dom, 'node': node})
        
        visited.append(node)
        for n in node.next:
            if n not in visited:
                getStateSetRec(n)

    getStateSetRec(root)
    return res

def getRoot(node : Graph) -> Graph:
    """
    Get the root node of the graph
    
    Args:
        node: Current node in the graph

    Returns:
        node: Root node of the graph
    """

    visited = set()
    
    def getRootRec(node):
        visited.add(node)
        if node.type == 'root':
            return node
        for n in node.prev:
            if n not in visited:
                return getRootRec(n)
            
    return getRootRec(node)

def getStateAction(node : Graph) -> Graph:
    """
    Get the state just before the action node in the graph

    Args:
        node: Current node in the graph

    Returns:
        node: State node just before the action node
    """

    visited = set()
    
    def getStateActionRec(node):
        visited.add(node)
        if node.type == 'state' or node.type == 'root':
            return node
        for n in node.prev:
            if n not in visited:
                return getStateActionRec(n)
            
    return getStateActionRec(node)

def getStateNode(driver : webdriver, current : Graph, workflow : list = []) -> tuple:
    """
    Get the state node in the graph, using the current URL and DOM, and if it already exists in the graph
    it returns the existing node, otherwise creates a new node and adds it to the graph

    Args:
        driver: Selenium WebDriver object
        current: Current state node in the graph
        workflow: List of nodes of the current workflow

    Returns:
        state: State node in the graph
        current: Current state node in the graph
    """

    dom = getDom(driver)
    state = driver.current_url

    if not current:
        current = Graph('root', previous=None, state=state, dom=dom, status='Success')
        workflow.append(current)
            
        return current, current
    
    S_set = getStateSet(getRoot(current))

    for s in S_set:
        # Check if the URL is the same
        if s['state'] != state:
            continue
        
        # Check if the DOM is the same, with a threshold of 0.8
        if GestaltPatternMatching(s['dom'], dom) > 0.8:
            if s['node'].id != getStateAction(current).id:
                current.next.append(s['node'])
                s['node'].prev.append(current)

            workflow.append(s['node'])
            return s['node'], current

    current = Graph('state', previous=current, state=state, dom=dom, status='Success')
    workflow.append(current)

    return current, current

def getActionsNode(driver, current : Graph) -> list:
    """
    Get the action nodes in the graph, using the DOM of the page to get the interactable elements,
    and if the action node already attached to the current state node, it returns the existing node,
    otherwise creates a new node and adds it to the graph

    Args:
        driver: Selenium WebDriver object
        current: Current state node in the graph

    Returns:
        node_actions: List of action nodes in the graph
    """

    actionList = getActions(driver)

    actionNodes = []

    for action in actionList:
        add = False
        for action_next in current.next:
            if action["locator"] == action_next.action["locator"]:
                actionNodes.append(action_next)
                add = True
                
        if not add:
            actionNodes.append(Graph('action', previous=current, action=action))

    return actionNodes