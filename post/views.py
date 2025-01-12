from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import *
# Create your views here.
def home(request):
    return render(request,'post/home.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PostForm


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Don't commit yet to add the user
            post.user = request.user  # Assign the current user
            post.save()  # Save the post object
            messages.success(request, "Your post has been uploaded")
            return redirect("user-profile", username=request.user)  # Redirect to the same page or another URL
    else:
        form = PostForm()

    return render(request, 'post/create_post.html', {'form': form})

def explore_users(request):
    explore = Post.objects.all()
    return render(request,"post/explore.html",{'explore':explore})

def like_post(request, post_id):
    me = User.objects.get(username = request.user)
    post = Post.objects.get(id = post_id)
    try:
        if not Like.objects.filter(user = me, post = post).exists():
            Like.objects.create(user = me, post = post)
        else:
            Like.objects.filter(user = me, post = post).delete()
        return redirect('explore-users')
    except Exception as e:
        messages.error(request,f"An error has occured : {e}")
        return redirect('explore-users')



    return render(request, 'post/comment_post.html', {'form': form, 'post': post})