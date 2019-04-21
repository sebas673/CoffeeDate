from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.models import Profile
from django.contrib import messages
import random
import threading

# handles the traffic from the homepage. Takes in a request arg and
# returns what we want the user to see when they are sent to this route.


# class Timer(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.event = threading.Event()

#     def run(self):
#         while not self.event.is_set():
#             print('hello')
#             num_of_days = 7
#             self.event.wait(num_of_days * 24 * 3600)

#     def stop(self):
#         self.event.set()


def home(request):
    if request.user.is_authenticated:
        user = request.user
        # makes the user pick their preferences
        if user.Profile.has_customized == False:
            messages.success(request, f'Finish customizing your profile')
            user.Profile.has_customized = True
            user.Profile.save()
            return redirect('profile')
        else:
            return render(request, 'match/home.html')
    else:
        return render(request, 'match/home.html')


def about(request):
    return render(request, 'match/about.html', {'title': 'About'})


def find_match(request):
    matching = random_match()
    for match in matching:
        user1, user2 = User.objects.get(id=match[0]), User.objects.get(id=match[1])
        set_match(user1, user2)
    return render(request, 'match/home.html')


def set_match(user1, user2):
    user1.Profile.mate_ID = user2.id
    user1.Profile.mate_firstname = user2.first_name
    user1.Profile.mate_lastname = user2.last_name
    user1.Profile.mate_personal_message = user2.Profile.personal_message
    user1.Profile.mate_image = user2.Profile.image
    user1.Profile.mate_email = user2.email
    user1.Profile.is_matched = True
    user1.Profile.save()

    user2.Profile.mate_ID = user1.id
    user2.Profile.mate_firstname = user1.first_name
    user2.Profile.mate_lastname = user1.last_name
    user2.Profile.mate_personal_message = user1.Profile.personal_message
    user2.Profile.mate_image = user1.Profile.image
    user2.Profile.mate_email = user1.email
    user2.Profile.is_matched = True
    user2.Profile.save()


def random_match():
    pairs = []
    user_ids = [user.id for user in User.objects.all().filter(Profile__is_matched='False')]
    print(user_ids)

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
