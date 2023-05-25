import json

teste = """{
    "0":{
        "Nome":"Will"
    },
    "1":{
        "Nome":"Pedro"
    }
}"""

# with open("teste.json", "w") as file:
#     data = file.write(teste)

# 1. Read file contents
with open("teste.json", "r") as file:
    data = json.load(file)

data.append({"Nome": "João"})

# teste.append({"Nome": "João"})

print(teste)