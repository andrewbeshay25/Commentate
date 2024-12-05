import requests

response = input("Choose request: ")

if response == '1':
    print(requests.get("http://127.0.0.1:8000").json())
elif response == '2':
    print(requests.get("http://127.0.0.1:8000/comments?name=Andrew").json())
elif response == '3':
    print(
    requests.post(
        "http://127.0.0.1:8000/",
        json={"id": 3, "message": "You suck at this!", "name": "Frank", "category": "roast"},
    ).json()
    )