import random
import aiohttp
import asyncio
import json
from faker import Faker

fake = Faker()


class User:
    def __init__(self, email, password, first_name, token=None):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.token = token

    @staticmethod
    def generate():
        return User(
            email=fake.email(),
            password=fake.password(length=8),
            first_name=fake.first_name()
        )


class Post:
    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id
        self.liked_by = []

    @staticmethod
    def generate(user_id):
        return Post(
            content=fake.sentence(nb_words=10),
            user_id=user_id
        )


class API:
    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session

    async def signup_user(self, user: User):
        url = f"{self.base_url}users/signup/"
        data = {
            "email": user.email,
            "password": user.password,
            "first_name": user.first_name
        }
        async with self.session.post(url, json=data) as response:
            response_data = await response.json()
            return response_data["user"]["id"]

    async def access_token(self, user: User):
        url = f"{self.base_url}users/login/"
        data = {
            "email": user.email,
            "password": user.password
        }
        async with self.session.post(url, data=data) as response:
            response_data = await response.json()
            user.token = response_data["access"]

    async def create_post(self, post: Post, token):
        url = f"{self.base_url}posts/create/"
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "content": post.content,
            "user": post.user_id,
            "liked_by": post.liked_by,
        }
        async with self.session.post(url, json=data, headers=headers) as response:
            print(f"Post Created: {response}")

    async def fetch_posts(self, token):
        url = f"{self.base_url}posts/posts/"
        headers = {"Authorization": f"Bearer {token}"}
        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                posts = await response.json()
                return [post["id"] for post in posts]
            else:
                print(f"Failed to fetch posts: {response.reason}")
                return []

    async def like_post(self, post_id, token):
        url = f"{self.base_url}posts/{post_id}/like/"
        headers = {"Authorization": f"Bearer {token}"}
        async with self.session.post(url, headers=headers) as response:
            if response.status == 200:
                print(f"Post Liked: {response}")
            else:
                print(f"Failed to like post: {response.reason}")


async def main():
    with open("config.json") as f:
        data = json.load(f)

    users_to_create = data.get("users")
    max_posts_per_user = data.get("max_posts_per_user")
    max_likes_per_user = data.get("max_likes_per_user")
    base_url = data.get("base_url")

    async with aiohttp.ClientSession() as session:
        api = API(base_url, session)
        users = [User.generate() for _ in range(users_to_create)]

        for user in users:
            user_id = await api.signup_user(user)
            await api.access_token(user)

            for _ in range(fake.random_int(min=1, max=max_posts_per_user)):
                post = Post.generate(user_id)
                await api.create_post(post, user.token)

            post_ids = await api.fetch_posts(user.token)

            for _ in range(fake.random_int(min=1, max=max_likes_per_user)):
                post_id = random.choice(post_ids)
                liking_user_token = random.choice([u.token for u in users])
                await api.like_post(post_id, liking_user_token)

asyncio.run(main())
