from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import About
from .forms import CollaborateRequestForm
from django.contrib import messages

# Create your views here.
def about_me(request):
    """
    Renders the About page
    """
    about = About.objects.all().order_by('-updated_on').first()

    if request.method == "POST":
        collaboratet_form = CollaborateRequestForm(data=request.POST)
        if collaboratet_form.is_valid():
            collaboratet_form.save()
            messages.add_message(request, messages.SUCCESS, "Collaboration request received! I endeavour to respond within 2 working days.")
        
    collaboratet_form = CollaborateRequestForm()

    return render(
        request,
        "about/about.html",
        {"about": about,
         "collaboratet_form": collaboratet_form,},
    )
    

    

    

