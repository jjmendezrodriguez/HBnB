import uuid
from datetime import datetime

class Review:
    def __init__(self, rating, comment, place, user):
        self.id = str(uuid.uuid4())
        self.rating = rating
        self.comment = comment
        self.place = place
        self.user = user
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def edit_review(self, new_rating, new_comment):
        self.rating = new_rating
        self.comment = new_comment
        self.updated_at = datetime.now()
