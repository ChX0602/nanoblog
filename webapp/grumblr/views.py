from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from grumblr.models import *
from grumblr.forms import *
from django.core import serializers
from django.http import HttpResponse
import datetime

# Create your views here.
@login_required
def home(request):
    user = request.user
    customUser = CustomUser.objects.get(user=user)
    followers = customUser.followers.all()
    blocked = customUser.blocked.all()
    comments = Comment.objects.all()
    profile = Profile.objects.get(owner=user)
    profiles = Profile.objects.all()
    posts = ((Post.objects.filter(user__in = followers))|(Post.objects.filter(user=user))).exclude(user__in = blocked).order_by('-date')
    post_form = PostForm()
    search_form = SearchForm()
    context = {'posts':posts, 'user':user, 'comments':comments, 'followers':followers, 'profile':profile, 'profiles':profiles, 'blocked':blocked, 'post_form':post_form, 'search_form':search_form}
    return render(request, 'grumblr/index.html', context)

@login_required
def add_post(request):
    form = PostForm(request.POST, request.FILES)
    if not form.is_valid():
        return redirect(reverse('home'))
    form.user = request.user
    profile = Profile.objects.get(owner=request.user)
    user_name = profile.first_name
    new_post = Post(text=form.cleaned_data['text'], user=request.user, user_name=user_name)
    new_post.save()
    postForm = PostForm(request.POST, request.FILES, instance=new_post)
    postForm.save()
    return redirect(reverse('home'))

@login_required
def add_comment(request, post_id, user_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        current_post = Post.objects.get(id=post_id)
        profile = Profile.objects.get(owner=request.user)
        user_name = profile.first_name
        new_comment = Comment(text = form.cleaned_data['text'], post = current_post,
                              commenter = request.user, commenter_name = user_name)
        new_comment.save()
        comments = Comment.objects.filter(post=current_post)
        response = serializers.serialize("json", comments)
        return HttpResponse(response, content_type="application/json")
    else:
        return redirect(reverse('home'))
        
@login_required
def dislike(request, post_id, user_id):
    poster = get_object_or_404(User, id=user_id)
    try:
        post = Post.objects.get(id=post_id, user=poster)
        profile = Profile.get_profiles(request.user)[0]
    except ObjectDoesNotExist:
        raise Http404
    post.dislikers.add(profile)
    post.save()
    return redirect(reverse('home'))
@login_required
def delete_post(request, id):
    errors = []
    # Deletes item if the logged-in user has an item matching the id
    try:
	post_to_delete = Post.objects.get(id=id, user=request.user)
	post_to_delete.delete()
    except ObjectDoesNotExist:
	errors.append('The post did not exist in your past grumblrs.')

    posts = Post.objects.filter(user=request.user)
    posts.reverse()
    context = {'posts' : posts, 'errors' : errors}
    return redirect(reverse('home'))

@transaction.atomic    
def register(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'grumblr/register.html', context)
    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'grumblr/register.html', context)
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'])
    new_user.is_active = False
    new_user.save()
    new_profile = Profile(owner=new_user)
    new_profile.save()
    customUser = CustomUser(user = new_user)
    customUser.save()

    token = default_token_generator.make_token(new_user)

    email_body = """
    Welcome to Grumblr! Please click the link below to activate your acount:
    http://%s%s
""" % (request.get_host(), 
       reverse('confirm', args=(new_user.username, token)))
    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="charlie+devnull@cs.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'grumblr/needs-confirmation.html', context)

@login_required
def followerStream(request):
     posts = Post.objects.exclude(user=request.user)
     profile = Profile.objects.get(owner = request.user)
     customUser = CustomUser.objects.get(user=request.user)
     comments = Comment.objects.all()
     followers = customUser.followers.all()
     blocked = customUser.blocked.all()
     otherUsers = User.objects.exclude(id=request.user.id)
     context = {'posts':posts, 'followers':followers, 'otherUsers': otherUsers, 'comments':comments, 'blocked':blocked, 'profile':profile}
     return render(request, 'grumblr/follower.html',context)

@login_required
def getProfile(request):
    profile = Profile.objects.get(owner = request.user)
    posts = Post.objects.filter(user=request.user)
    context = {'profile':profile, 'posts': posts}
    return render(request, 'grumblr/profile.html', context)

@login_required
def get_follower_profile(request, id):
    try:
        fuser = User.objects.get(id=id)
        profile = Profile.objects.get(owner = fuser)
        posts = Post.objects.filter(user = fuser)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'grumblr/follower_profile.html', {'profile':profile, 'posts':posts})

@login_required
@transaction.commit_on_success
def add_profile(request):
    if request.method == "GET":
        context = {'form':ProfileForm()}
        return render(request, 'grumblr/add_profile.html',context)
    new_profile = Profile(owner=request.user)
    form = ProfileForm(request.POST, request.FILES, instance=new_profile)
    if not form.is_valid():
        context = {'form':form}
        return render(request, 'grumblr/add_profile.html', context)
    form.save()
    return redirect(reverse('home'))

@login_required
@transaction.atomic
def edit_profile(request, id):
    try:
        profile_to_edit = get_object_or_404(Profile, owner=request.user, id=id)
    except ObjectDoesNotExist:
        raise Http404
    if request.method == 'GET':
        form = ProfileForm(instance=profile_to_edit)
        context = {'form':form, 'id':id, 'user':request.user}
        return render(request, 'grumblr/edit_profile.html', context)
    form = ProfileForm(request.POST, request.FILES, instance=profile_to_edit)
    if not form.is_valid():
        context = {'form':form, 'id':id}
        return render(request, 'grumblr/edit_profile.html', context)
    form.save()
    return redirect(reverse('home'))

@login_required
def add_follower(request, id):
    user_to_add = get_object_or_404(User, id=id)
    custom_user = CustomUser.objects.get(user = request.user)
    custom_user.followers.add(user_to_add)
    custom_user.save()
    return redirect(reverse('home'))

@login_required
def block_follower(request, id):
    user_to_block = get_object_or_404(User, id=id)
    custom_user = CustomUser.objects.get(user = request.user)
    custom_user.blocked.add(user_to_block)
    custom_user.save()
    return redirect(reverse('home'))


@login_required
def search(request):
    form = SearchForm(request.POST)
    if not form.is_valid():
        return redirect(reverse('home'))
    keyword = form.cleaned_data['searchField']

    matchedPosts = Post.objects.filter(text__icontains=keyword)
    matchedUsers = ((Profile.objects.filter(first_name__icontains=keyword)) | (Profile.objects.filter(last_name__icontains=keyword)))
    return render(request, 'grumblr/search_result.html', {'matchedPosts':matchedPosts, 'matchedUsers':matchedUsers, 'user':request.user})        
@login_required
def get_photo(request, id, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, owner=user)
    if not profile.picture:
        raise Http404
    content_type = guess_type(profile.picture.name)
    return HttpResponse(profile.picture, content_type=content_type)

@login_required
def get_post_photo(request, post_id):
    post = get_object_or_404(Post,id=post_id)
    if not post.picture:
        raise Http404
    content_type = guess_type(post.picture.name)
    return HttpResponse(post.picture, content_type=content_type)
    
    
    
@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'grumblr/confirmed.html', {})

def get_grumbles(request):
    now = datetime.datetime.now()
    desired_time = now - datetime.timedelta(seconds=10)
    response_text = serializers.serialize("json", Post.objects.filter(date__gte=desired_time))
    return HttpResponse(response_text, content_type="application/json")
