from flask import Flask
import urllib.request
import json

app = Flask(__name__)


def get_categories(categorie):
    if type(categorie) != str:
        return None
    with urllib.request.urlopen(
            "https://www.10bis.co.il/NextApi/GetRestaurantMenu?culture=en&uiCulture=en&restaurantId=19156&deliveryMethod=pickup") as url:
        data = json.loads(url.read().decode())
        index = None
        for i in range(len(data["Data"]["categoriesList"])):
            if data["Data"]["categoriesList"][i]["categoryName"] == categorie:
                index = i
        if index is not None:
            data_categories = data["Data"]["categoriesList"][index]
            return json.dumps(data_categories["dishList"])
        else:
            return None


def get_specific(categorie, id):
    data = json.loads(get_categories(categorie))
    index = None
    for i in range(len(data)):
        if data[i]["dishId"] == int(id):
            index = i
    if index is not None:
        data_id = data[index]
        return json.dumps(data_id)
    else:
        return None


@app.route("/")
def home():
    return """Welcome:
           To watch all the drinks: /drinks
           To watch a specific drinks: /drink/ + id
           To watch all the drinks: /pizzas
           To watch a specific drinks: /pizza/ + id
           To watch all the drinks: /desserts
           To watch a specific drinks: /dessert/ + id
           To order: /order + drinks: + ids, pizzas: + ids, desserts: + ids"""


@app.route("/drinks")
def drinks():
    return get_categories("Drinks")


@app.route("/drink/<id>")
def drink_id(id):
    drink = get_specific("Drinks", id)
    if drink is not None:
        return drink
    else:
        return "Not found"


@app.route("/pizzas")
def pizzas():
    return get_categories("Pizzas")


@app.route("/pizza/<id>")
def pizza_id(id):
    pizza = get_specific("Pizzas", id)
    if pizza is not None:
        return pizza
    else:
        return "Not found"


@app.route("/desserts")
def desserts():
    return get_categories("Desserts")


@app.route("/dessert/<id>")
def dessert_id(id):
    dessert = get_specific("Desserts", id)
    if dessert is not None:
        return dessert
    else:
        return "Not found"


@app.route("/order/", defaults={"drinks": None, "pizzas": None, "desserts": None}, methods=["POST"])
def order(drinks, pizzas, desserts):
    price = 0
    for i, j, k in zip(drinks, pizzas, desserts):
        price += int(json.loads(get_specific("Drinks", i))["dishPrice"])
        price += int(json.loads(get_specific("Pizzas", j))["dishPrice"])
        price += int(json.loads(get_specific("Desserts", k))["dishPrice"])
    result = {
        'price': price
    }
    return json.dumps(result)


if __name__ == "__main__":
    app.run(debug=True)
