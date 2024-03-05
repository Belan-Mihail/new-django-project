from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from .models import Post, Comment
from .forms import CommentForm
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
class PostList(generic.ListView):
    # queryset = Post.objects.all()
    queryset = Post.objects.filter(status=1)
    # queryset = Post.objects.filter(author=2)
    # Post.objects.all().order_by("created_on")
    # template_name = "post_list.html"
    template_name = "blog/index.html"
    paginate_by = 6

# второй параметр соответсвует значению пути в урл <slug:slug> второму слаг
def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`
    """

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()
    
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )
        
    comment_form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {"post": post, 
         'coder': 'Mike',
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
        },
        # value post from 31 ... key what we use in template
        # coder and Mike = new context what i add
    )
    
    
    # Other ways of creating context
    
    # def post_detail(request, slug):

    # queryset = Post.objects.filter(status=1)
    # post = get_object_or_404(queryset, slug=slug)

    # context = {"post": post}

    # return render(
    #     request,
    #     "blog/post_detail.html",
    #     context
    # )
    
    
    # alt with int
    # path("<int:event_id>/", views.event_detail, name="event_detail")
    
    # def event_detail(request, event_id):
    
    # queryset = Event.objects.all()
    # event = get_object_or_404(queryset, event_id=event_id)
    
    # shortly == passing the model directly into the helper function
    # event = get_object_or_404(Event, event_id=event_id)

    # return render(
    #     request,
    #     "events/event_detail.html",
    #     {"event": event}
    # )
    

def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))

def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))