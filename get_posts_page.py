import requests
import json

r = requests.get("""https://graph.facebook.com/v3.2/431851910256044/posts?access_token=EAADOyPLBYsIBAFdkZCwOBv1Jo7Ek97Firrh89h7nnqobckD5iZCIwWv5Qvki7Dwme1LP8983HgJQF99VpAVAqJkC5Gsyvcwgk7mvdUcZCai1Rq0fKGFVjwXRpu42diSATELFXpsHv077fhcJoOXC3XUf5C1YycUVgDOa4S8putEs3ZCtGA5dDAL8jshyj8QCu1uUoFqwk1Gt3UYjHFkYJbRcjXDJQBRibjuzo6helwZDZD""")
next = "will contain address of next page"

while(next!="null"):
    data = r.json()
    jsonData = data["data"]
    for item in jsonData:
        name = item.get("message")
        id = item.get("id")
        print("""Post id:""")
        print(id)
        print("""Message:""")
        print(name)
        print("\n")
    next = data["paging"]["next"]
