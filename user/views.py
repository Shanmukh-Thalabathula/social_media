from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm
from .models import Profile



def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if not User.objects.filter(username=username).exists():
                messages.error(request, "User does not exist!")
                return redirect('user-login')

            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, "Incorrect password!")
                return redirect('user-login')
            else:
                login(request, user)
                messages.success(request, f"Welcome {user.username}")
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'user/user_login.html', {'form': form})

@login_required(login_url='user-login')
def user_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out...")
    return redirect('user-login')


def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken!")
                return redirect('user-register')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already taken!")
                return redirect('user-register')

            # Create the user instance first
            user = form.save()

            # Now create the profile instance and associate it with the user
            profile = Profile.objects.create(user=user)

            profile.save()
            messages.success(request, "Account created successfully...")
            return redirect('user-login')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/user_registration.html', {'form': form})

@login_required(login_url='user-login')
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = user.post_set.all()  # Assuming a related_name is defined in the Post model

    # Check if the logged-in user is following this profile
    is_following = profile.followers.filter(id=request.user.id).exists()

    return render(request, 'user/profile.html', {
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
        'followers_count': profile.followers.count(),
        'following_count': profile.following.count(),
    })


@login_required(login_url='user-login')
def edit_user_profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        bio = request.POST.get('bio', '').strip()
        profile_picture = request.FILES.get('profile_picture')

        # Check for unique username and email
        if User.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, f"Oops! It seems '{username}' already exists.")
            return redirect("edit-user-profile")
        if User.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, f"Oops! It seems '{email}' already exists.")
            return redirect("edit-user-profile")

        # Update user fields
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        # Update profile fields
        if profile_picture:
            profile.profile_picture = profile_picture
        profile.bio = bio
        profile.save()

        messages.success(request, "Your profile has been updated.")
        return redirect("user-profile",username = request.user)

    return render(request, 'user/edit_profile.html' )

@login_required(login_url='user-login')
def follow(request, username):
    me = request.user  # Current logged-in user
    others = get_object_or_404(User, username=username)  # Target user to follow

    my_profile = Profile.objects.get(user=me)
    others_profile = Profile.objects.get(user=others)

    my_profile.following.add(others)  # Add target user to 'following' list
    others_profile.followers.add(me)  # Add logged-in user to target's 'followers' list

    messages.success(request, f"You are now following {username}.")
    return redirect('user-profile', username=username)


@login_required(login_url='user-login')
def unfollow(request, username):
    me = request.user  # Current logged-in user
    others = get_object_or_404(User, username=username)  # Target user to unfollow

    my_profile = Profile.objects.get(user=me)
    others_profile = Profile.objects.get(user=others)

    my_profile.following.remove(others)  # Remove target user from 'following' list
    others_profile.followers.remove(me)  # Remove logged-in user from target's 'followers' list

    messages.success(request, f"You have unfollowed {username}.")
    return redirect('user-profile', username=username)



