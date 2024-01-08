from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse
from .models import Blog
from .forms import BlogForm

@login_required
def index(request):
    blogs = Blog.objects.all()
    template = loader.get_template('blogs/index.html')
    context = {'blogs': blogs}
    return HttpResponse(template.render(context, request))

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.user = request.user  # Set the current user as the blog owner
            new_blog.save()
            return redirect('index')
    else:
        form = BlogForm()

    return render(request, 'blogs/create_blog.html', {'form': form})

def detail(request, blog_id):
    return HttpResponse("you are looking at blog %s." % blog_id)

def login_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('index')