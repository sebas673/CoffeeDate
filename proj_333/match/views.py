from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import Profile
import random
import threading

# handles the traffic from the homepage. Takes in a request arg and
# returns what we want the user to see when they are sent to this route.


class Timer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def run(self):
        while not self.event.is_set():
            print('hello')
            num_of_days = 7
            self.event.wait(num_of_days * 24 * 3600)

    def stop(self):
        self.event.set()


def home(request):
    return render(request, 'match/home.html')


def about(request):
    return render(request, 'match/about.html', {'title': 'About'})


def find_match(request):
    matching = random_match()
    for match in matching:
        user1, user2 = User.objects.get(id=match[0]), User.objects.get(id=match[1])
        set_match(user1, user2)
    return render(request, 'match/home.html')

# helper function


def set_match(user1, user2):
    user1.profile.mate_ID = user2.id
    user1.profile.mate_firstname = user2.first_name
    user1.profile.mate_lastname = user2.last_name
    user1.profile.mate_personal_message = user2.profile.personal_message
    user1.profile.mate_image = user2.profile.image
    user1.profile.mate_email = user2.email
    user1.profile.is_matched = True
    user1.profile.save()

    user2.profile.mate_ID = user1.id
    user2.profile.mate_firstname = user1.first_name
    user2.profile.mate_lastname = user1.last_name
    user2.profile.mate_personal_message = user1.profile.personal_message
    user2.profile.mate_image = user1.profile.image
    user2.profile.mate_email = user1.email
    user2.profile.is_matched = True
    user2.profile.save()


# helper function


def random_match():
    pairs = []
    user_ids = [user.id for user in User.objects.all()]

    random.shuffle(user_ids)

    i = 0
    j = 0
    numUsers = len(user_ids)
    while i < numUsers - 1:
        pairs.append([user_ids[i], user_ids[i + 1]])
        i += 2

    # odd number of users case
    if numUsers % 2 == 1:
        pairs.append([user_ids[0], user_ids[numUsers - 1]])

    return pairs
