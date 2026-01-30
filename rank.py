# ranks.py
RANKS = [
    {"id": 1, "name": "Новичок 🐍", "min_stars": 0, "color": "#808080"},
    {"id": 2, "name": "Показушник 💫", "min_stars": 100, "color": "#00FF00"},
    {"id": 3, "name": "Сжигатель 🔥", "min_stars": 1000, "color": "#FF4500"},
    {"id": 4, "name": "Охотник 🎯", "min_stars": 5000, "color": "#1E90FF"},
    {"id": 5, "name": "Мастер 🏅", "min_stars": 10000, "color": "#FFD700"},
    {"id": 6, "name": "Император 👑", "min_stars": 50000, "color": "#FF0000"}
]

def get_user_rank(spent_stars):
    for rank in reversed(RANKS):
        if spent_stars >= rank["min_stars"]:
            return rank
    return RANKS[0]
