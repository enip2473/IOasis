import requests, os, random, asyncio, userdata, time

problems = []

def init(): # get all problems on codeforces
    global problems
    r = requests.get(url = "https://codeforces.com/api/problemset.problems")
    problems = r.json()["result"]["problems"]
    print("Cf Data OK!")

def query(tag : str, rating : int): # return a list of problems with specific tag and ratings
    result = []
    tag = tag.lower()
    for problem in problems:
        try:
            if problem['rating'] == rating and tag in problem["tags"]:
                result.append("{}/{}".format(problem['contestId'], problem['index']))
        except:
            pass
    return result

# if found return the time of that submission, else return -1
def status(user : str):
    url = "https://codeforces.com/api/user.status?handle={}&from=1&count=5".format(user)
    print(url)
    r = requests.get(url = url)
    print(r.status_code)
    result = r.json()["result"]
    return result

def check_verdict(handle : str, problemname : str, verdict : str):
    result = status(handle)
    for res in result:
        name = "{}/{}".format(res["problem"]["contestId"], res["problem"]["index"])
        if res["verdict"] == verdict and name == problemname:
            return res["creationTimeSeconds"]
    return -1

if __name__ == "__main__":
    print(status("enip"))
    
