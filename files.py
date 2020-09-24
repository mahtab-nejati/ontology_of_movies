import os
import requests
import json


def getResponse(url, thePath, theFile):

    cwd = os.getcwd()
    base = os.path.join(cwd, 'responses')
    thePath = os.path.join(base, thePath)

    try:
        respFile = open('{fileN}.html'.format(
            fileN=os.path.join(thePath, theFile)), 'r')
        resp = respFile.read()
        respFile.close()
    except (FileNotFoundError):
        resp = requests.get(url).text
        try:
            os.makedirs(thePath, exist_ok=True)
        except FileExistsError:
            pass
        respFile = open('{fileN}.html'.format(
            fileN=os.path.join(thePath, theFile)), 'w+')
        respFile.write(resp)
        respFile.close()
    return resp


def readJson():
    try:
        with open('data/data.json') as jsonFile:
            return json.loads(jsonFile.read())
    except FileNotFoundError:
        return []


def getStartIndex():
    already = readJson()
    try:
        lastAlready = int(already[-1]['rank'])
    except:
        lastAlready = 0
    return int(lastAlready/10)


def saveToJson(new):
    togo = readJson() + new
    cwd = os.getcwd()
    thePath = os.path.join(cwd, 'data')
    try:
        os.makedirs(thePath, exist_ok=True)
    except FileExistsError:
        pass
    with open('data/data.json', 'w') as jsonFile:
        json.dump(togo, jsonFile, indent=4)


def saveOWL(res, fName):
    cwd = os.getcwd()
    thePath = os.path.join(cwd, 'ontology')
    try:
        os.makedirs(thePath, exist_ok=True)
    except FileExistsError:
        pass
    with open('ontology/'+fName, 'w') as rdfFile:
        rdfFile.write(res)


def getOntology(fName):
    thePath = os.path.join(os.getcwd(), 'ontology')
    thePath = os.path.join(thePath, fName)
    try:
        with open(thePath, 'r') as f:
            content = f.read()
    except:
        content = ""
    return content
