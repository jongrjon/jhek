from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Post, Status, Tag


def post_list(request):
    posts = Post.objects.listed()
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, slug: str):
    post = get_object_or_404(Post, slug=slug)
    # Draft is never served. Private only to staff or author. Unlisted is reachable by slug.
    if post.status == Status.DRAFT:
        raise Http404
    if post.status == Status.PRIVATE and not (
        request.user.is_authenticated
        and (request.user.is_staff or post.author_id == request.user.id)
    ):
        raise Http404
    return render(request, "blog/post_detail.html", {"post": post})


def tag_view(request, name: str):
    tag = get_object_or_404(Tag, name=name)
    posts = Post.objects.listed().filter(tags=tag)
    return render(request, "blog/tag.html", {"tag": tag, "posts": posts})
