
class Comment:

    def __init__(self, id, user, username, recipe, comment, comment_date, edited, ratings):
        self.id = id
        self.user = user
        self.username = username
        self.recipe = recipe
        self.comment = comment
        self.comment_date = comment_date
        self.edited = edited
        self.ratings = ratings
        self.rating = self.getRatings()
    
    def getRatings(self):
        count = 0
        for key in self.ratings.keys():
            count += int(self.ratings[key])
        return count
    
    def __repr__(self):
        return f"User ID : {self.user}\nRecipe ID : {self.recipe}\nComment : {self.comment}\nComment Date : {self.comment_date}\nEdited : {self.edited}"