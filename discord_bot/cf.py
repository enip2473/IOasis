import requests

problems = []

def init(): # get all problems on codeforces
    global problems
    r = requests.get(url = "https://codeforces.com/api/problemset.problems")
    ori = r.json()["result"]["problems"]
    for problem in ori:
        try:
            problems.append(("{}/{}".format(problem['contestId'], problem['index']), problem["rating"], problem["tags"]))
        except:
            pass
    print("Cf Data OK!")

def query(tag : str, rating : int): # return a list of problems with specific tag and ratings
    # problem[0] : name, problem[1] : rating, problem[2] : tags
    result = [problem for problem in problems if problem[1] == rating]
    if tag == "all":
        return result
    else:
        result = [problem for problem in result if tag in problem[2]]
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

def change_rating(user_rating : int, problem_rating : int, solved : bool):
    print(user_rating, problem_rating)
    prob = 1 / (1 + (10 ** ((problem_rating - user_rating) / 400)))
    
    base = min((problem_rating - user_rating) // 2, 100)
    
    dif = round(base * (-prob + int(solved)))
    
    change = ("+" if dif > 0 else "")
    res_str = "{} -> {} ({}{})\n".format(user_rating, user_rating + dif, change, dif)
    return res_str, dif

def get_problem(problemname : str):
    for name, rating, tags in problems:
        if name == problemname:
            return rating, tags
    return 0, 0

if __name__ == "__main__":
    print(status("enip"))
    
