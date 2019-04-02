from django.shortcuts import render

matchMate = [
    {
        'name': 'Sebastian',
        'personalMessage': '"I really want to meet you!"',
        'expires': 'May 12, 2019'
    },
    
]

# handles the traffic from the homepage. Takes in a request arg and
# returns what we want the user to see when they are sent to this route.


def home(request):
    context = {
        'matchMate': matchMate
    }
    return render(request, 'match/home.html', context)


def about(request):
    return render(request, 'match/about.html', {'title': 'About'})
