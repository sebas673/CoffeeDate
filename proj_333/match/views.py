from django.shortcuts import render

# handles the traffic from the homepage. Takes in a request arg and
# returns what we want the user to see when they are sent to this route.


def home(request):
    return render(request, 'match/home.html')


def about(request):
    return render(request, 'match/about.html', {'title': 'About'})
