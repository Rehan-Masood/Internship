import requests
from flask import Flask, render_template
from post import Post

app = Flask(__name__)

FALLBACK_POSTS = [
    {
        "id": 1,
        "title": "The Life of Cactus",
        "subtitle": "Who knew that cacti lived such interesting lives.",
        "body": "Nori grape silver beet broccoli kombu beet greens fava bean potato quandong celery. Bunya nuts black-eyed pea prairie turnip leek lentil turnip greens parsnip."
    },
    {
        "id": 2,
        "title": "Top 15 Things to do When You are Bored",
        "subtitle": "Are you bored? Don't know what to do? Try these top 15 activities.",
        "body": "Chase ball of string eat plants. meow, and throw up because I ate plants going to catch the red dot today going to catch the red dot today."
    },
    {
        "id": 3,
        "title": "Introduction to Intermittent Fasting",
        "subtitle": "Learn about the newest health craze.",
        "body": "Cupcake ipsum dolor. Sit amet marshmallow topping cheesecake muffin. Halvah croissant candy canes bonbon candy. Apple pie jelly beans topping carrot cake."
    }
]


def fetch_blog_posts():
    """Fetches posts from API safely with fallback data if API fails."""
    api_url = "https://api.npoint.io/c790b4d5cca5802068a4"
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            posts_list = data.get("posts", data) if isinstance(data, dict) else data
            return [Post(p["id"], p["title"], p["subtitle"], p["body"]) for p in posts_list]
    except Exception as e:
        print(f"⚠️ API fetch failed ({e}). Using local fallback data.")
    
    return [Post(p["id"], p["title"], p["subtitle"], p["body"]) for p in FALLBACK_POSTS]


post_objects = fetch_blog_posts()


@app.route("/")
def get_all_posts():
    return render_template("index.html", all_posts=post_objects)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
            break
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)