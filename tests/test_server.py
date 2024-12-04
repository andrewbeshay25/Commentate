import requests

response = input("Choose request: ")

if response == '1':
    print(requests.get("http://127.0.0.1:8000").json())
elif response == '2':
    print(requests.get("http://127.0.0.1:8000/comments?name=Andrew").json())