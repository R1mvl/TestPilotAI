from flask import Flask, send_from_directory, request
import asyncio
import threading

from src.api.service import runWebTesting, getTests, getResult, generateTest, process_queue, cancelTestQueue

app = Flask(__name__, static_folder="../ui")

@app.route("/home")
def serve_home():
    return send_from_directory(app.static_folder + "/home", "index.html")


@app.route("/result")
def serve_result():
    return send_from_directory(app.static_folder + "/result", "index.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route("/api/run", methods=["POST"])
def run_api():
    code = runWebTesting(request.get_json())
    
    return "", code

@app.route("/api/cancel", methods=["POST"])
def cancel_api():
    code = cancelTestQueue(request.get_json()["id"])

    return "", code

@app.route("/api/gettests", methods=["GET"])
def get_test():
    return getTests()

@app.route("/api/result", methods=["GET"])
def get_result():
    id = request.args.get("id")

    element = getResult(id)

    if element is None:
        return "", 404
    else:
        return element

@app.route("/api/generateTest", methods=["GET"])
def generateTestPlaywright():
    testId = request.args.get("id")
    nodeId = request.args.get("nodeId")
    language = request.args.get("language")

    print("idTest", testId)
    print("idNode", nodeId)
    print("language", language)

    res = {
        "code": generateTest(testId, nodeId, language)
    }

    return res


loop = asyncio.get_event_loop()
t = threading.Thread(target=loop.run_until_complete, args=(process_queue(),))
t.start()
    
#app.run(debug=False)
