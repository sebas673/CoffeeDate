from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import Profile
from django.contrib import messages
import random
import threading
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Group

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
            context = {
                'groups': Group.objects.all()
            }
            return render(request, 'match/home.html', context)
    else:
        return render(request, 'match/home.html')


def about(request):
    return render(request, 'match/about.html', {'title': 'About'})


# class GroupListView(ListView):
#     model = Group
#     user = self.User
#     template_name = 'match/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'groups'
#     ordering = ['-date_created']


class GroupDetailView(DetailView):
    model = Group


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['group_name', 'group_image', 'group_description', 'members']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class GroupUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Group
    fields = ['group_name', 'group_image', 'group_description', 'members']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        group = self.get_object()
        if self.request.user == group.owner:
            return True
        return False


class GroupDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Group
    success_url = '/'

    def test_func(self):
        group = self.get_object()
        if self.request.user == group.owner:
            return True
        return False


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
