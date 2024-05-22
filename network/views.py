from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import Post, Follower

from .models import User


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# API Handlers
@csrf_exempt
@login_required
def posts(request):
  """
  API view to create a new post.
  """
  if request.method == 'POST':
    # Check if user is authenticated
    if not request.user.is_authenticated:
      return JsonResponse({'error': 'Authentication required'}, status=401)

    # Parse request data
    try:
      data = json.loads(request.body)
      content = data.get('content')
      print(content)
    except Exception as e:
      return JsonResponse({'error': 'Invalid data format'}, status=400)

    # Validate content
    if not content:
      return JsonResponse({'error': 'Content cannot be empty'}, status=400)

    # Create new post
    user = get_user_model().objects.get(username=request.user.username)
    new_post = Post.objects.create(user=user, content=content)

    # Return success response
    return JsonResponse({'message': 'Post created successfully', 'id': new_post.id}, status=201)
  elif request.method == 'GET':
    all_posts = Post.objects.all().order_by('-timestamp')  # Order by latest first

    return render(request, 'network/all_posts.html', {
        'posts': all_posts
    })
  else:
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def profile(request, username):
  # Get the user with the given username
  user = get_object_or_404(User, username=username)

  # Get all posts for the user
  user_posts = Post.objects.filter(user=user).order_by('-timestamp')

  # Get follower count for the user
  follower_count = user.followers.count()

  # Get following count for the user (optional)
  following_count = user.following.count()  # Optional, depending on your model
  
  # Check if the user is viewing their own profile
  show_follow_button = request.user != user and request.user.is_authenticated

  # Check if current user is following the profile user (if logged in)
  following = False
  if show_follow_button:
    following = Follower.objects.filter(follower=request.user, following=user).exists()

  return render(request, 'network/profile.html', {
      'profile_user': user,
      'posts': user_posts,
      'follower_count': follower_count,
      'following_count': following_count,
      'following': following,
      'show_follow_button': show_follow_button
  })