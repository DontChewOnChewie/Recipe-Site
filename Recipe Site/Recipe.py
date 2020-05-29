import json

'''
Class used as a model for Recipe.
Used on both account and recipe pages of site.
'''
class Recipe:

    def __init__(self, id, name, description, ingredients, creator):
        self.id = int(id)
        self.name = name
        self.description = description
        self.ingredients = json.loads(ingredients)
        self.creator = creator

    def __repr__(self):
        return f"ID : {self.id}\nName : {self.name}\nDescription : {self.description}\nIngredients : {self.ingredients}\nCreator : {self.creator}"