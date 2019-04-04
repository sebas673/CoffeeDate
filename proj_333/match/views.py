from django.shortcuts import render

posts = [
    {
        'author': 'sebas1',
        'title': 'Post 1',
        'content': 'first post content',
        'date_posted': 'April 1, 2019'
    },
    {
        'author': 'sebas2',
        'title': 'Post 2',
        'content': 'second post content',
        'date_posted': 'April 2, 2019'
    }
]

# handles the traffic from the homepage. Takes in a request arg and
# returns what we want the user to see when they are sent to this route.


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'match/home.html', context)


def about(request):
    return render(request, 'match/about.html', {'title': 'About'})
