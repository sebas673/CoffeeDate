from django.shortcuts import render
import threading

# handles the traffic from the homepage. Takes in a request arg and
# returns what we want the user to see when they are sent to this route.


class Timer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def run(self):
        while not self.event.is_set():
            # this is the event to do
            print('hello')
            num_of_days = 7
            self.event.wait(num_of_days * 24 * 3600)

    def stop(self):
        self.event.set()


def home(request):
    return render(request, 'match/home.html')


def about(request):
    return render(request, 'match/about.html', {'title': 'About'})
