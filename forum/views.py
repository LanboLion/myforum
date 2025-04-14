from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseForbidden
from .models import Post, Comment, Mention
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User

def index(request):
    order_by = request.GET.get('order_by', '-created_at')
    post_list = Post.objects.all().order_by(order_by)
    paginator = Paginator(post_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'forum/index.html', {
        'page_obj': page_obj,
        'order_by': order_by
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'forum/post_form.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            mentions = extract_mentions(comment.content)
            for username in mentions:
                try:
                    user = User.objects.get(username=username)
                    Mention.objects.create(user=user, comment=comment)
                except User.DoesNotExist:
                    pass
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()
    
    return render(request, 'forum/post_detail.html', {
        'post': post,
        'form': form,
        'comments': post.comment_set.filter(parent_comment__isnull=True)
    })

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({
        'liked': liked,
        'total_likes': post.total_likes()
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user.is_superuser:
        comment.delete()
    return redirect('post_detail', pk=comment.post.id)

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not request.user.is_superuser:
        return HttpResponseForbidden("无权删除此帖子")
    post.delete()
    return redirect('index')

def extract_mentions(text):
    import re
    return re.findall(r'@(\w+)', text)