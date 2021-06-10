import requests

problems = []

def init(): # get all problems on codeforces
    global problems
    r = requests.get(url = "https://codeforces.com/api/problemset.problems")
    problems = r.json()["result"]["problems"]

def query(tag : str, rating : int): # return a list of problems with specific tag and ratings
    global problems
    result = []
    tag = tag.lower()
    for problem in problems:
        try:
            if problem['rating'] == rating and tag in problem["tags"]:
                result.append("{}/{}".format(problem['contestId'], problem['index']))
        except:
            pass
    print(result)


if __name__ == "__main__":
    init()
    query("dp", 1900)
    
