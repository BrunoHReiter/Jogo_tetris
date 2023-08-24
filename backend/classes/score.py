from config import *

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pontos = db.Column(db.Integer)

    def __str__(self):
        return f"ID: {self.id}, Pontos: {self.pontos}"

    def json(self):
        return {
            "id": self.id,
            "pontos": self.pontos
        }