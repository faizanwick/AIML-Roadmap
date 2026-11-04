import requests

url = "https://api.github.com/search/repositories"

params = {
    "q" : "python data engineering",
    "sort" : "stars",
    "order" : "desc"
}

response = requests.get(url, params=params, timeout=10)

# if response.status_code == 200:
#     data = response.json()

#     print("Username: ", data["login"])
#     print("Repositories: ", data["public_repos"])

if response.status_code == 200:
    data = response.json()
    for repo in data["items"][:5]:
        print(repo["full_name"], repo["stargazers_count"])

else:
    print("Request failed: ", response.status_code)