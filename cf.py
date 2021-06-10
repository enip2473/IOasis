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
    return result

def status(user : str):
    url = "https://codeforces.com/api/user.status?handle={}&from=1&count=5".format(user)
    r = requests.get(url = url)
    result = r.json()["result"]
    ans = []
    for res in result:
        ans.append((res["verdict"], "{}/{}".format(res["problem"]['contestId'], res["problem"]['index'])))
    print(ans)
    return ans



if __name__ == "__main__":
    #init()
    #query("dp", 1900)
    print(status("enip"))
    
