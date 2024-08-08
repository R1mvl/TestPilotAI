def seleniumTestgenerator(website, test):
    print("GENERATE TEST")

    finalCode = ""
    finalCode += "from selenium import webdriver\n"
    finalCode += "from selenium.webdriver.common.by import By\n"
    finalCode += "from selenium.webdriver.chrome.options import Options\n"
    finalCode += "from selenium.webdriver.support.ui import WebDriverWait\n"
    finalCode += "from selenium.webdriver.support import expected_conditions as EC\n"
    finalCode += "import chromedriver_autoinstaller\n"
    finalCode += "from time import sleep\n\n"

    finalCode += "nodeList = " + str(test["nodes"]) + "\n"
    finalCode += "loginURL = '" + website["loginURL"] + "'\n"
    finalCode += "loginPatterns = " + str(website["loginPatterns"]) + "\n"
    finalCode += "websiteURL = '" + website["websiteURL"] + "'\n"
    finalCode += "targetURL = '" + website["targetURL"] + "'\n\n"

    finalCode += "chromedriver_autoinstaller.install()\n"
    finalCode += "chrome_options = Options()\n\n"

    finalCode += "driver = webdriver.Chrome(options=chrome_options)\n"
    finalCode += "wait = WebDriverWait(driver, 10)\n\n"

    finalCode += "def perform_login():\n"
    finalCode += "    for pattern in loginPatterns:\n"
    finalCode += "        if pattern['type'] == 'input':\n"
    finalCode += "            wait.until(EC.presence_of_element_located((By.XPATH, pattern['XPath']))).send_keys(pattern['value'])\n"
    finalCode += "        elif pattern['type'] == 'click':\n"
    finalCode += "            wait.until(EC.element_to_be_clickable((By.XPATH, pattern['XPath']))).click()\n\n"

    finalCode += "# Open the website\n"
    finalCode += "driver.get(websiteURL)\n\n"

    finalCode += "for node in nodeList:\n"
    finalCode += "    # Check if the page is the login page\n"
    finalCode += "    if driver.current_url == loginURL:\n"
    finalCode += "        perform_login()\n\n"
    finalCode += "    if node['type'] in ['root', 'state']:\n"
    finalCode += "        # Check if the state is \"Error : new window opened\" and test if a new window is opened\n"
    finalCode += "        if node['state'] == 'Error : new window opened':\n"
    finalCode += "            if len(driver.window_handles) > 1:\n"
    finalCode += "                print('Test passed')\n"
    finalCode += "            else:\n"
    finalCode += "                print('Test failed : new window not opened')\n"
    finalCode += "            break\n\n"
    finalCode += "        # Check if the state is \"Error : page not loaded\" and test if the page is not loaded\n"
    finalCode += "        if node['state'] == 'Error : page not loaded':\n"
    finalCode += "            if driver.execute_script('return document.readyState') != 'complete':\n"
    finalCode += "                print('Test passed')\n"
    finalCode += "            else:\n"
    finalCode += "                print('Test failed : page loaded')\n"
    finalCode += "            break\n\n"
    finalCode += "        # Check if the state is \"Goal reached\" and test if the current URL is the target URL\n"
    finalCode += "        if node['state'] == 'Goal reached':\n"
    finalCode += "            if driver.current_url == targetURL:\n"
    finalCode += "                print('Test passed')\n"
    finalCode += "            else:\n"
    finalCode += "                print('Test failed : goal not reached ' + driver.current_url + ' != ' + targetURL)\n"
    finalCode += "            break\n\n"
    finalCode += "        # Check if the state is \"Error : error in the console\" and test if the error is present in the console\n"
    finalCode += "        if node['state'] == 'Error : error in the console':\n"
    finalCode += "            if driver.execute_script('return document.querySelector(\".error\")') is not None:\n"
    finalCode += "                print('Test passed')\n"
    finalCode += "            else:\n"
    finalCode += "                print('Test failed : error not found in the console')\n"
    finalCode += "            break\n\n"
    finalCode += "        # Check if the current URL is the same as the state URL\n"
    finalCode += "        if driver.current_url != node['state']:\n"
    finalCode += "            print(f\"Test failed : {driver.current_url} != {node['state']}\")\n"
    finalCode += "            break\n\n"
    finalCode += "    elif node['type'] == 'action':\n"
    finalCode += "        # Process the action\n"
    finalCode += "        element = wait.until(EC.element_to_be_clickable((By.XPATH, node['state'])))\n\n"
    finalCode += "        if node['process'] is None:\n"
    finalCode += "            element.click()\n"
    finalCode += "        else:\n"
    finalCode += "            element.send_keys(node['process'])\n\n"
    finalCode += "    # Wait for the page to load\n"
    finalCode += "    sleep(1)\n\n"

    finalCode += "driver.quit()\n"


    return finalCode

def playwrightPythonTestGenerator(website, test):
    print("GENERATE TEST")

    finalCode = ""
    finalCode += "from playwright.sync_api import sync_playwright\n"
    finalCode += "from time import sleep\n\n"

    finalCode += "nodeList = " + str(test["nodes"]) + "\n"
    finalCode += "loginURL = '" + website["loginURL"] + "'\n"
    finalCode += "loginPatterns = " + str(website["loginPatterns"]) + "\n"
    finalCode += "websiteURL = '" + website["websiteURL"] + "'\n"
    finalCode += "targetURL = '" + website["targetURL"] + "'\n\n"

    finalCode += "def perform_login(page):\n"
    finalCode += "    for pattern in loginPatterns:\n"
    finalCode += "        if pattern['type'] == 'input':\n"
    finalCode += "            page.fill(pattern['XPath'], pattern['value'])\n"
    finalCode += "        elif pattern['type'] == 'click':\n"
    finalCode += "            page.click(pattern['XPath'])\n\n"

    finalCode += "with sync_playwright() as p:\n"
    finalCode += "    browser = p.chromium.launch()\n"
    finalCode += "    context = browser.new_context()\n"
    finalCode += "    page = context.new_page()\n\n"

    finalCode += "    # Open the website\n"
    finalCode += "    page.goto(websiteURL)\n\n"

    finalCode += "    for node in nodeList:\n"
    finalCode += "        # Check if the page is the login page\n"
    finalCode += "        if page.url == loginURL:\n"
    finalCode += "            perform_login(page)\n\n"
    finalCode += "        if node['type'] in ['root', 'state']:\n"
    finalCode += "            # Check if the state is \"Error : new window opened\" and test if a new window is opened\n"
    finalCode += "            if node['state'] == 'Error : new window opened':\n"
    finalCode += "                new_page = None\n"
    finalCode += "                try:\n"
    finalCode += "                    new_page = context.wait_for_event('page')\n"
    finalCode += "                    print('Test passed')\n"
    finalCode += "                except:\n"
    finalCode += "                    print('Test failed : no new window opened')\n"
    finalCode += "                break\n\n"
    finalCode += "            # Check if the state is \"Error : page not loaded\" and test if the page is not loaded\n"
    finalCode += "            if node['state'] == 'Error : page not loaded':\n"
    finalCode += "                if page.evaluate('document.readyState') != 'complete':\n"
    finalCode += "                    print('Test passed')\n"
    finalCode += "                else:\n"
    finalCode += "                    print('Test failed : page loaded')\n"
    finalCode += "                break\n\n"
    finalCode += "            # Check if the state is \"Goal reached\" and test if the current URL is the target URL\n"
    finalCode += "            if node['state'] == 'Goal reached':\n"
    finalCode += "                if page.url == targetURL:\n"
    finalCode += "                    print('Test passed')\n"
    finalCode += "                else:\n"
    finalCode += "                    print('Test failed : goal not reached ' + page.url + ' != ' + targetURL)\n"
    finalCode += "                break\n\n"
    finalCode += "            # Check if the state is \"Error : error in the console\" and test if the error is present in the console\n"
    finalCode += "            if node['state'] == 'Error : error in the console':\n"
    finalCode += "                console_errors = page.evaluate(\"window.console.error()\");\n"
    finalCode += "                if console_errors:\n"
    finalCode += "                    print('Test passed')\n"
    finalCode += "                else:\n"
    finalCode += "                    print('Test failed : error not found in the console')\n"
    finalCode += "                break\n\n"
    finalCode += "            # Check if the current URL is the same as the state URL\n"
    finalCode += "            if page.url != node['state']:\n"
    finalCode += "                print(f\"Test failed : {page.url} != {node['state']}\")\n"
    finalCode += "                break\n\n"
    finalCode += "        elif node['type'] == 'action':\n"
    finalCode += "            # Process the action\n"
    finalCode += "            if node['process'] is None:\n"
    finalCode += "                page.click(node['state'])\n"
    finalCode += "            else:\n"
    finalCode += "                page.fill(node['state'], node['process'])\n\n"
    finalCode += "        # Wait for the page to load\n"
    finalCode += "        sleep(1)\n\n"

    finalCode += "    browser.close()\n"

    return finalCode

def playwrightTestGeneratorJava(website, test):
    print("GENERATE TEST")

    finalCode = ""
    finalCode += "package com.amadeus.playwright.maestro.test.base;\n"
    finalCode += "import com.microsoft.playwright.*;\n"
    finalCode += "import java.util.List;\n\n"

    finalCode += "public class PlaywrightTest {\n"
    finalCode += "    public static void main(String[] args) {\n"
    finalCode += "        try (Playwright playwright = Playwright.create()) {\n"
    finalCode += "            Browser browser = playwright.chromium().launch(new BrowserType.LaunchOptions().setHeadless(false));\n"
    finalCode += "            BrowserContext context = browser.newContext();\n"
    finalCode += "            Page page = context.newPage();\n\n"

    finalCode += "            String loginURL = \"" + website["loginURL"].replace('"', '\\"') + "\";\n"
    finalCode += "            String websiteURL = \"" + website["websiteURL"].replace('"', '\\"') + "\";\n"
    finalCode += "            String targetURL = \"" + website["targetURL"].replace('"', '\\"') + "\";\n\n"

    finalCode += "            String[][] loginPatterns = {\n"
    for pattern in website["loginPatterns"]:
        if pattern["type"] == "input":
            finalCode += "                    {\"" + pattern["type"] + "\", \"" + pattern["XPath"].replace('"', '\\"') + "\", \"" + pattern["value"].replace('"', '\\"') + "\"},\n"
        elif pattern["type"] == "click":
            finalCode += "                    {\"" + pattern["type"] + "\", \"" + pattern["XPath"].replace('"', '\\"') + "\", null},\n"
    finalCode = finalCode.rstrip(",\n") + "\n"
    finalCode += "            };\n\n"

    finalCode += "            Object[][] nodes = {\n"
    for node in test["nodes"]:
        finalCode += "                    {" + str(node["id"]) + ", \"" + node["type"] + "\", \"" + node["state"].replace('"', '\\"') + "\", " + (f"\"{node['process']}\"" if node["process"] is not None else "null") + ", \"" + (node["status"].replace('"', '\\"') if node["status"] is not None else "null") + "\"},\n"
    finalCode = finalCode.rstrip(",\n") + "\n"
    finalCode += "            };\n\n"

    finalCode += "            page.navigate(websiteURL);\n\n"

    finalCode += "            for (Object[] node : nodes) {\n"
    finalCode += "                String nodeType = (String) node[1];\n"
    finalCode += "                String nodeState = (String) node[2];\n"
    finalCode += "                String nodeProcess = (String) node[3];\n\n"

    finalCode += "                if (page.url().equals(loginURL)) {\n"
    finalCode += "                    performLogin(page, loginPatterns);\n"
    finalCode += "                }\n\n"

    finalCode += "                if (nodeType.equals(\"root\") || nodeType.equals(\"state\")) {\n"
    finalCode += "                    if (nodeState.equals(\"Error : new window opened\")) {\n"
    finalCode += "                        // detect if there is more than one window open\n"
    finalCode += "                        List<Page> pages = context.pages();\n"
    finalCode += "                        if (pages.size() > 1) {\n"
    finalCode += "                            System.out.println(\"Test failed : new window opened\");\n"
    finalCode += "                        } else {\n"
    finalCode += "                            System.out.println(\"Test passed\");\n"
    finalCode += "                        }\n"
    finalCode += "                        break;\n"
    finalCode += "                    } else if (nodeState.equals(\"Error : page not loaded\")) {\n"
    finalCode += "                        if (!page.evaluate(\"document.readyState\").equals(\"complete\")) {\n"
    finalCode += "                            System.out.println(\"Test passed\");\n"
    finalCode += "                        } else {\n"
    finalCode += "                            System.out.println(\"Test failed : page loaded\");\n"
    finalCode += "                        }\n"
    finalCode += "                        break;\n"
    finalCode += "                    } else if (nodeState.equals(\"Goal reached\")) {\n"
    finalCode += "                        if (page.url().equals(targetURL)) {\n"
    finalCode += "                            System.out.println(\"Test passed\");\n"
    finalCode += "                        } else {\n"
    finalCode += "                            System.out.println(\"Test failed : goal not reached \" + page.url() + \" != \" + targetURL);\n"
    finalCode += "                        }\n"
    finalCode += "                        break;\n"
    finalCode += "                    } else if (nodeState.equals(\"Error : error in the console\")) {\n"
    finalCode += "                        if (page.locator(\".error\").isVisible()) {\n"
    finalCode += "                            System.out.println(\"Test passed\");\n"
    finalCode += "                        } else {\n"
    finalCode += "                            System.out.println(\"Test failed : error not found in the console\");\n"
    finalCode += "                        }\n"
    finalCode += "                        break;\n"
    finalCode += "                    } else if (!page.url().equals(nodeState)) {\n"
    finalCode += "                        System.out.println(\"Test failed : \" + page.url() + \" != \" + nodeState);\n"
    finalCode += "                        break;\n"
    finalCode += "                    }\n"
    finalCode += "                } else if (nodeType.equals(\"action\")) {\n"
    finalCode += "                    if (nodeProcess == null) {\n"
    finalCode += "                        page.click(nodeState);\n"
    finalCode += "                    } else {\n"
    finalCode += "                        page.fill(nodeState, nodeProcess);\n"
    finalCode += "                    }\n"
    finalCode += "                }\n"
    finalCode += "                Thread.sleep(1000);\n"
    finalCode += "            }\n"
    finalCode += "            browser.close();\n"
    finalCode += "        } catch (InterruptedException e) {\n"
    finalCode += "            e.printStackTrace();\n"
    finalCode += "        }\n"
    finalCode += "    }\n"

    finalCode += "    public static void performLogin(Page page, String[][] loginPatterns) {\n"
    finalCode += "        for (String[] pattern : loginPatterns) {\n"
    finalCode += "            if (pattern[0].equals(\"input\")) {\n"
    finalCode += "                page.fill(pattern[1], pattern[2]);\n"
    finalCode += "            } else if (pattern[0].equals(\"click\")) {\n"
    finalCode += "                page.click(pattern[1]);\n"
    finalCode += "            }\n"
    finalCode += "        }\n"
    finalCode += "    }\n"

    finalCode += "}\n"

    return finalCode

def playwrightTestGeneratorJavaScript(website, test):
    final_code = ""

    final_code += "const { chromium } = require('playwright');\n\n"
    final_code += "async function runTest() {\n"
    final_code += "    const browser = await chromium.launch({ headless: false });\n"
    final_code += "    const context = await browser.newContext();\n"
    final_code += "    const page = await context.newPage();\n\n"

    l = website['loginURL'].replace('\"', '\\\"')
    final_code += f"    const loginURL = \"{l}\";\n"
    l = website['websiteURL'].replace('\"', '\\\"')
    final_code += f"    const websiteURL = \"{l}\";\n"
    l = website['targetURL'].replace('\"', '\\\"')
    final_code += f"    const targetURL = \"{l}\";\n\n"

    final_code += "    const loginPatterns = [\n"
    for pattern in website["loginPatterns"]:
        Xp = pattern["XPath"].replace('\"', '\\\"')

        if pattern["type"] == "input":
            val = pattern["value"].replace('\"', '\\\"')
            final_code += f"        ['input', \"{Xp}\", \"{val}\"],\n"
        elif pattern["type"] == "click":
            final_code += f"        ['click', \"{Xp}\", null],\n"
    final_code = final_code.rstrip(",\n") + "\n"
    final_code += "    ];\n\n"

    final_code += "    const nodes = [\n"
    for node in test["nodes"]:
        st = node["state"].replace('"', '\\"')
        process = f"\"{node['process']}\"" if node['process'] is not None else "null"
        status = f"\"{node['status']}\"" if node['status'] is not None else "null"
        final_code += f"        [{node['id']}, \"{node['type']}\", \"{st}\", {process}, {status}],\n"

    final_code = final_code.rstrip(",\n") + "\n"
    final_code += "    ];\n\n"

    final_code += "    await page.goto(websiteURL);\n\n"

    final_code += "    for (const node of nodes) {\n"
    final_code += "        const nodeType = node[1];\n"
    final_code += "        const nodeState = node[2];\n"
    final_code += "        const nodeProcess = node[3];\n\n"

    final_code += "        if (page.url() === loginURL) {\n"
    final_code += "            await performLogin(page, loginPatterns);\n"
    final_code += "        }\n\n"

    final_code += "        if (nodeType === 'root' || nodeType === 'state') {\n"
    final_code += "            if (nodeState === 'Error : new window opened') {\n"
    final_code += "                // detect if there is more than one window open\n"
    final_code += "                const pages = await context.pages();\n"
    final_code += "                if (pages.length > 1) {\n"
    final_code += "                    console.log('Test passed');\n"
    final_code += "                } else {\n"
    final_code += "                    console.log('Test failed : new window opened');\n"
    final_code += "                }\n"
    final_code += "                break;\n"
    final_code += "            } else if (nodeState === 'Error : page not loaded') {\n"
    final_code += "                if (!(await page.evaluate(() => document.readyState === 'complete'))) {\n"
    final_code += "                    console.log('Test passed');\n"
    final_code += "                } else {\n"
    final_code += "                    console.log('Test failed : page loaded');\n"
    final_code += "                }\n"
    final_code += "                break;\n"
    final_code += "            } else if (nodeState === 'Goal reached') {\n"
    final_code += "                if (page.url() === targetURL) {\n"
    final_code += "                    console.log('Test passed');\n"
    final_code += "                } else {\n"
    final_code += "                    console.log(`Test failed : goal not reached ${page.url()} != ${targetURL}`);\n"
    final_code += "                }\n"
    final_code += "                break;\n"
    final_code += "            } else if (nodeState === 'Error : error in the console') {\n"
    final_code += "                const errorVisible = await page.isVisible('.error');\n"
    final_code += "                if (errorVisible) {\n"
    final_code += "                    console.log('Test passed');\n"
    final_code += "                } else {\n"
    final_code += "                    console.log('Test failed : error not found in the console');\n"
    final_code += "                }\n"
    final_code += "                break;\n"
    final_code += "            } else if (page.url() !== nodeState) {\n"
    final_code += "                console.log(`Test failed : ${page.url()} != ${nodeState}`);\n"
    final_code += "                break;\n"
    final_code += "            }\n"
    final_code += "        } else if (nodeType === 'action') {\n"
    final_code += "            if (nodeProcess === null) {\n"
    final_code += "                await page.click(nodeState);\n"
    final_code += "            } else {\n"
    final_code += "                await page.fill(nodeState, nodeProcess);\n"
    final_code += "            }\n"
    final_code += "        }\n"
    final_code += "        await page.waitForTimeout(1000);\n"
    final_code += "    }\n"

    final_code += "    await browser.close();\n"
    final_code += "}\n\n"

    final_code += "async function performLogin(page, loginPatterns) {\n"
    final_code += "    for (const pattern of loginPatterns) {\n"
    final_code += "        if (pattern[0] === 'input') {\n"
    final_code += "            await page.fill(pattern[1], pattern[2]);\n"
    final_code += "        } else if (pattern[0] === 'click') {\n"
    final_code += "            await page.click(pattern[1]);\n"
    final_code += "        }\n"
    final_code += "    }\n"
    final_code += "}\n\n"

    final_code += "runTest();\n"

    return final_code

def robotTestGenerator(website, test):
    print("GENERATE TEST")

    # Generate the .robot file content
    robotCode = "*** Settings ***\n"
    robotCode += "Library    Browser\n"
    robotCode += "Variables    variables.py\n\n"

    robotCode += "*** Test Cases ***\n"
    robotCode += "Test Website\n"
    robotCode += "    New Page    ${WEBSITE_URL}\n"
    robotCode += "    FOR    ${pattern}    IN    @{loginPatterns}\n"
    robotCode += "        ${type}    Set Variable    ${pattern}[type]\n"
    robotCode += "        ${XPath}    Set Variable    ${pattern}[XPath]\n"
    robotCode += "        Run Keyword If    '${type}' == 'click'    Click    ${XPath}\n"
    robotCode += "        ...    ELSE IF    '${type}' == 'input'    Input Text    ${XPath}    ${pattern}[value]\n"
    robotCode += "    END\n\n"

    robotCode += "    FOR    ${node}    IN    @{NODES}\n"
    robotCode += "        ${id}    Set Variable    ${node}[id]\n"
    robotCode += "        ${type}    Set Variable    ${node}[type]\n"
    robotCode += "        ${state}    Set Variable    ${node}[state]\n"
    robotCode += "        ${process}    Set Variable    ${node}[process]\n"
    robotCode += "        ${status}    Set Variable    ${node}[status]\n\n"

    robotCode += "        Run Keyword If    '${type}' == 'root' or '${type}' == 'state'\n"
    robotCode += "        ...    Run Keyword If    '${state}' == 'Error : new window opened' and Evaluate    len(self.get_browser().contexts) > 1\n"
    robotCode += "        ...    Log    Test passed\n"
    robotCode += "        ...    ELSE    Log    Test failed : new window not opened\n"
    robotCode += "        ...    ELSE IF    '${state}' == 'Error : page not loaded' and Evaluate    self.get_browser().is_page_loaded() != True\n"
    robotCode += "        ...    Log    Test passed\n"
    robotCode += "        ...    ELSE    Log    Test failed : page loaded\n"
    robotCode += "        ...    ELSE IF    '${state}' == 'Goal reached' and Evaluate    self.get_browser().get_page_url() == '${TARGET_URL}'\n"
    robotCode += "        ...    Log    Test passed\n"
    robotCode += "        ...    ELSE    Log    Test failed : goal not reached\n"
    robotCode += "        ...    ELSE IF    '${state}' == 'Error : error in the console' and Evaluate    self.get_browser().check_for_console_error() == True\n"
    robotCode += "        ...    Log    Test passed\n"
    robotCode += "        ...    ELSE    Log    Test failed : error not found in the console\n"
    robotCode += "        ...    ELSE    Run Keyword If    self.get_browser().get_page_url() != '${state}'\n"
    robotCode += "        ...    Log    Test failed : URL mismatch\n\n"

    robotCode += "        Run Keyword If    '${type}' == 'action'\n"
    robotCode += "        ...    Run Keyword If    ${process} is None\n"
    robotCode += "        ...    Click    ${state}\n"
    robotCode += "        ...    ELSE    Input Text    ${state}    ${process}\n"
    robotCode += "        Sleep    1s\n"
    robotCode += "    END\n\n"

    robotCode += "    Close Browser\n"

    # Generate the variables.py file content
    variablesCode = "loginURL = '" + website["loginURL"] + "'\n"
    variablesCode += "websiteURL = '" + website["websiteURL"] + "'\n"
    variablesCode += "targetURL = '" + website["targetURL"] + "'\n\n"

    variablesCode += "loginPatterns = [\n"
    for pattern in website["loginPatterns"]:
        Xpath = pattern["XPath"].replace('"', '\\"')
        if pattern["type"] == "input":
            value = pattern["value"].replace('"', '\\"')
            variablesCode += "    {'type': 'input', 'XPath': '" + Xpath + "', 'value': '" + value + "'},\n"
        elif pattern["type"] == "click":
            variablesCode += "    {'type': 'click', 'XPath': '" + Xpath + "'},\n"

    variablesCode = variablesCode.rstrip(",\n") + "\n"
    variablesCode += "]\n\n"

    variablesCode += "nodes = [\n"
    for node in test["nodes"]:
        state = node["state"].replace('"', '\\"')
        process = f"\"{node['process']}\"" if node['process'] is not None else "None"
        status = f"\"{node['status']}\"" if node['status'] is not None else "None"
        variablesCode += "    { 'id': " + str(node["id"]) + ", 'type': '" + node["type"] + "', 'state': '" + state + "', 'process': " + process + ", 'status': " + status + " },\n"
    variablesCode = variablesCode.rstrip(",\n") + "\n"
    variablesCode += "]\n"

    return {"robot": robotCode, "variables": variablesCode}

