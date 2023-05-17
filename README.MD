# Django Social App

This is a social app built with Django Rest Framework where users can sign up, create posts, and like posts. 

## Starting the Server

To start the Django server, navigate to the project root directory and run the following command:

```bash
python3 manage.py runserver
```

```bash
python3 aiohttp_requests.py
```


## Models

### User
This model extends Django's `AbstractBaseUser` and `PermissionsMixin` to provide custom fields for our application, including `email`, `first_name`, `last_name`, `default_language`, `gender`, `age`, `is_active`, `is_staff`, `is_superuser`, and `date_joined`.

### UserActivity
This model tracks the last login and last request time of a user.

### Post
This model represents a user post, containing `user`, `content`, and `created_at` fields.

### PostLike
This model represents a like on a post, containing `post`, `user`, and `liked_at` fields. A `PostLike` object is created whenever a user likes a post.

## Views

### User Views
- `SignupView`: Users can sign up with their details.
- `LoginView`: Users can log in to their account.
- `LastLoginView`: Users can view their last login time.
- `LastRequestView`: Users can view their last request time.

### Post Views
- `PostListView`: View all posts.
- `PostCreateView`: Create a new post.
- `LikeUnlikePostView`: Like or unlike a post.
- `PostLikesAnalyticView`: View analytics on post likes.

## API Endpoints

### User Endpoints
- `api/users/signup/` (POST): Sign up a new user.
- `api/users/login/` (POST): Log in an existing user.
- `api/users/<int:pk>/last-login/` (GET): Get the last login time of the user with the given ID.
- `api/users/<int:pk>/last-request/` (GET): Get the last request time of the user with the given ID.

### Post Endpoints
- `posts/all/` (GET): Get a list of all posts.
- `posts/create/` (POST): Create a new post.
- `posts/<int:pk>/like/` (POST): Like or unlike the post with the given ID.
- `/posts/analytics/?date_from=2023-05-15&date_to=2023-05-18` (GET): Get analytics data on post likes.

All API endpoints require an `Authorization` header with a valid token obtained from the `login/` endpoint.

Example: `'Authorization': 'Bearer {access_token}'`


## Python Script for Testing
We also provide a Python script that uses the Faker library and asyncio to create a number of fake users, posts, and likes. This can be used for testing and demo purposes.

## Installation and Running

1. Clone the repository.
2. Install the required packages from `requirements.txt` using pip.
3. Run the Django server.
4. Use the provided Python script to populate the app with test data if needed.
