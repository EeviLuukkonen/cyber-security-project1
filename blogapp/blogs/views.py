from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Blog, Comment
from .forms import CommentForm
from django.db import connection

def index(request):
    blogs = Blog.objects.all()
    template = loader.get_template('blogs/index.html')
    context = {'blogs': blogs}
    return HttpResponse(template.render(context, request))

@login_required
# FLAW 2 CSRF:
@csrf_exempt
# REMOVE CSRF_EXEMPT TO FIX
def create_blog(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        author = request.POST.get('author')
        url = request.POST.get('url')

        # FLAW 1 SQL INJECTION:
        query = f"INSERT INTO blogs_blog (name, author, year, url, user_id) VALUES ('{name}', '{author}', '{timezone.now()}', '{url}', {request.user.id});"
        with connection.cursor() as cursor:
            cursor.execute(query)

        # here is a fix to the SQL vulnerability:
        # new_blog = Blog(name=name, author=author, year=timezone.now(), url=url, user=request.user)
        # new_blog.save()
        return redirect('index')
    else:
        return render(request, 'blogs/create_blog.html')

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog)
    comment_form = CommentForm()
    if request.method == 'POST':
        print(request.POST)
        if 'delete_blog' in request.POST:
            # FLAW 4: BROKEN ACCESS CONTROL
            blog.delete()
            messages.success(request, f'Blog {blog.name} deleted successfully.')
            '''
            FLAW 4 FIX:
                if 'delete_blog' in request.POST:
                    print("delete blog submitted")
                    if request.user.is_superuser:
                        blog.delete()
                        messages.success(request, f'Blog {blog.name} deleted successfully.')
                        return redirect('index')
                    else:
                        messages.error(request, 'You do not have permission to delete this blog.')
            '''
            return redirect('index')
        elif 'content' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.blog = blog
                new_comment.user = request.user
                new_comment.save()
                return redirect('detail', blog_id=blog_id)
        elif 'delete_comment' in request.POST:
            if request.user.is_superuser:
                comment_id = request.POST.get('delete_comment')
                comment_to_delete = get_object_or_404(Comment, pk=comment_id)
                comment_to_delete.delete()
                messages.success(request, 'Comment deleted successfully.')
                return redirect('detail', blog_id=blog_id)
            else:
                messages.error(request, 'You do not have permission to delete this comment.')
    return render(request, 'blogs/detail.html', {'blog': blog, 'comments': comments, 'comment_form': comment_form})

def login_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('index')