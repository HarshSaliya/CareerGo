from django.shortcuts import render, get_object_or_404
from .models import BlogPost, QuestionAnswer

def blog_page(request, slug=None):
    if slug:
        post = get_object_or_404(BlogPost, slug=slug)
        questions = QuestionAnswer.objects.filter(blog_post=post)
    else:
        post = None
        questions = None

    posts = BlogPost.objects.all()
    return render(request, 'blog_page.html', {'posts': posts, 'post': post, 'questions': questions})
