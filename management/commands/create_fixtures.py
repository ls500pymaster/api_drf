import json
from random import choice, randint

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from faker import Faker

from apps.posts.models import Post

User = get_user_model()
fake = Faker()


class CreateFixtures(BaseCommand):
	help = "Create random users, posts, likes using JSON config."

	def add_arguments(self, parser):
		parser.add_arguments("config.json", type=str, help="JSON file with config.")

	def handle(self, *args, **kwargs):
		json_file = kwargs["config.json"]
		with open(json_file, "r") as file:
			config = json.load(file)

		number_of_users = config["number_of_users"]
		max_posts_per_user = config["max_posts_per_user"]
		max_likes_per_user = config["max_likes_per_user"]

		users = [User(username=fake.name(), email=fake.email(), password=fake.password()) for _ in
				range(number_of_users)]
		User.objects.bulk_create(users)

		posts = []
		for user in User.objects.all():
			post_count = randint(1, max_posts_per_user)
			for _ in range(post_count):
				posts.append(Post(
					user=user,
					content=fake.sentense()
				))
		Post.objects.bulk_create(posts)

		all_posts = Post.objects.all()
		for user in User.objects.all():
			like_count = randint(1, max_likes_per_user)
			for _ in range(like_count):
				post = choice(all_posts)
				post.liked_by.add(user)

		self.stdout.write(self.style.SUCCESS("Fixtures created successfully."))
