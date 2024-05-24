from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Post, Follower, Like, User
from django.core.paginator import Paginator

def index(request):
  if request.user.is_authenticated:
    return render(request, "network/index.html")
  else:
      return render(request, "network/login.html")


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


def profile(request, username):
  # Get the user with the given username
  user = get_object_or_404(User, username=username)

  # Get all posts for the user
  user_posts = Post.objects.filter(user=user).order_by('-timestamp')
  posts = []
  for post in user_posts:
    already_liked = post.liked_by.filter(user=request.user).exists()
    posts.append({
      'post': post,
      'already_liked': already_liked
      })

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
      'posts': posts,
      'follower_count': follower_count,
      'following_count': following_count,
      'following': following,
      'show_follow_button': show_follow_button
  })

@login_required
def following_posts(request):  
  if request.method != 'GET':
    return JsonResponse({'error': 'Method not allowed'}, status=405)
  
  # Get users the current user is following
  following = request.user.following.all()
  
  # Get actual User objects from following list
  following_users = [f.following for f in following]
  
  # Get all posts from users being followed
  following_posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')
  posts = []
  for post in following_posts:
    already_liked = post.liked_by.filter(user=request.user).exists()
    posts.append({
      'post': post,
      'already_liked': already_liked
      })
    
  paginator = Paginator(posts, 10)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(request, 'network/all_posts.html', {
    'posts': page_obj,
    'paginator': paginator    
    })
  
  
# API Handlers
@csrf_exempt
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
    all_posts = Post.objects.all().prefetch_related('liked_by').order_by('-timestamp') 
    posts = []
    for post in all_posts:
      already_liked = post.liked_by.filter(user=request.user).exists()
      posts.append({
        'post': post,
        'already_liked': already_liked,
        })
      
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'network/all_posts.html', {
      'posts': page_obj,
      'paginator': paginator
    })
    
  else:
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
@csrf_exempt
def edit_post(request, post_id):
  """
  API view to edit a particular post.
  """    
  if request.method != 'PUT':
    return JsonResponse({'error': 'Method not allowed'}, status=405)
  
  post = get_object_or_404(Post, pk=post_id)
  
  # Ensure user can only edit their own posts (security check)
  if not post.user == request.user:
    return JsonResponse({'error': 'Can\'t edit others\' post.'}, status=403)

  # Parse request data
  data = json.loads(request.body)
  new_content = data.get('new_content')
  
  if not new_content:
    return JsonResponse({'error': 'Invalid data format'}, status=400)    
  
  try:
    post.content = new_content
    post.save()
    # Return success response
    return JsonResponse({'message': 'Post updated successfully' }, status=200)
  
  except Exception as e:
    return JsonResponse({'error': 'Error updating Database!'}, status=500)


@csrf_exempt
@login_required
def follow(request, username):
  """
  API view to follow or unfollow a particular user.
  """
  if request.method != 'POST':
    return JsonResponse({'error': 'Method not allowed'}, status=405)
  else:
    # Check if user is authenticated
    if not request.user.is_authenticated:
      return JsonResponse({'error': 'Authentication required'}, status=401)

    # Parse request data
    try:
      data = json.loads(request.body)
      to_be_followed = data.get('follow')
      user_to_follow = get_object_or_404(User, username=username)
      
    except Exception as e:
      return JsonResponse({'error': 'Invalid data format'}, status=400)

    # Validate content
    if not username or not user_to_follow:
      return JsonResponse({'error': 'Wrong username to be followed'}, status=400)
    
    if request.user == user_to_follow: 
      return JsonResponse({'error': 'A user can\'t follow themselves'}, status=400)

    followers_count = user_to_follow.followers.count()
     
    # Follow or Unfollow
    if to_be_followed:
      follower = Follower.objects.create(follower=request.user, following=user_to_follow)
      
      followers_count += 1
      
      # Return success response
      return JsonResponse({'message': 'User followed successfully', 'followers_count': followers_count }, status=200)
    else:
      follower = Follower.objects.filter(follower=request.user, following=user_to_follow)
      if follower.exists():
        follower.delete()

        followers_count -= 1
        
        # Return success response
        return JsonResponse({'message': 'User unfollowed successfully', 'followers_count': followers_count }, status=200)
      else:
        return JsonResponse({'error': 'Already not following'}, status=400)
    
    
@login_required
def like(request, post_id):
  """
  API view to like or unlike a particular post.
  """
  post = get_object_or_404(Post, pk=post_id)
    
  # Check for existing like and update accordingly
  like, created = Like.objects.get_or_create(user=request.user, post=post)
  
  if not created:  # Unlike scenario (existing like record)
    like.delete()
    post.likes -= 1
  else:  # Like scenario (new like record)
    post.likes += 1
  post.save()
  like_count = post.likes
  
  return HttpResponse(like_count)