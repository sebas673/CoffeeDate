from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import Profile, Prefs
from django.contrib import messages
import random
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Group, Pair
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from itertools import permutations
import numpy as np


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
                'groups_member': Group.objects.all().filter(members=user.Profile).exclude(owner=user),
                'groups_owner': Group.objects.all().filter(owner=user),
                'pairs': Pair.objects.all().filter(pair_1=user.id) | Pair.objects.all().filter(pair_2=user.id)
            }
        return render(request, 'match/home.html', context)
    else:
        return render(request, 'match/home.html')


def about(request):
    return render(request, 'match/about.html', {'title': 'About'})

def faq(request):
    return render(request, 'match/faq.html', {'title': 'Frequently Asked Questions'})

# We can use this is we want to see ALL of the groups
# class GroupListView(ListView):
#     model = Group
#     user = self.User
#     template_name = 'match/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'groups'
#     ordering = ['-date_created']


class GroupDetailView(DetailView):
    model = Group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pairs'] = Pair.objects.filter(pair_group=self.object)
        return context


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name', 'group_image', 'group_description', 'members']
    members = forms.ModelMultipleChoiceField(queryset=Profile.objects.all(), widget=forms.CheckboxSelectMultiple())


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    # fields = ['group_name', 'group_image', 'group_description', 'members']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class GroupUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Group
    form_class = GroupForm
    # fields = ['group_name', 'group_image', 'group_description', 'members']

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



class PrefsForm(forms.ModelForm):
    CHOICES=[(1,'Strongly Disagree'), (2,'Somewhat Disagree'), (3, 'Neutral'), (4, 'Somewhat Agree'), (5, 'Strongly Agree')]

    class Meta:
        model = Prefs
        fields = ['pref1', 'pref2', 'pref3', 'pref4', 'pref5', 'pref6', 'pref7', 'pref8', 'pref9', 'pref10']

    q1 = 'You often spend time exploring unrealistic yet intriguing ideas.'
    q2 = 'You often think about what you should have said in a conversation long after it has taken place.' 
    q3 = 'You enjoy vibrant social events with lots of people.' 
    q4 = 'I would never cheat on my taxes.' 
    q5 = 'You are more of a detail-oriented than a big picture person.' 
    q6 = 'You have a careful and methodical approach to life.'
    q7 = 'In your opinion, it is sometimes OK to step on others to get ahead in life.'
    q8 = 'You usually lose interest in a discussion when it gets philosophical.'
    q9 = 'You feel more drawn to places with a bustling and busy atmosphere than to more quiet and intimate ones.'
    q10 = 'I handle tasks methodically.'  

    pref1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q1)
    pref2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q2)
    pref3 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q3)
    pref4 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q4)
    pref5 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q5)
    pref6 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q6)
    pref7 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q7)
    pref8 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q8)
    pref9 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q9)
    pref10 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q10)


class PrefsDetailView(DetailView):
    model = Prefs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prefs'] = Prefs.objects.filter(user=self.request.user)
        return context


class PrefsCreateView(LoginRequiredMixin, CreateView):
    model = Prefs
    form_class = PrefsForm
    # fields = ['pref1', 'pref2', 'pref3', 'pref4', 'pref5']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PrefsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Prefs
    form_class = PrefsForm
    # fields = ['pref1', 'pref2', 'pref3', 'pref4', 'pref5']
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        prefs = self.get_object()
        if self.request.user == prefs.user:
            return True
        return False


# matches all the members
# @login_required
# @user_passes_test(lambda u: u.is_superuser)
def match_all(request):

    # reset all users
    for user in User.objects.all():
        user.Profile.is_matched = False
#---------------------------------------------------------------------------------------------------------------------

    users = [user for user in User.objects.all().filter(Profile__is_matched='False')] # Profile needs to change to Prefs?
    matching = full_match(users)
    for match in matching:
        set_match(match[0], match[1])
        set_match(match[1], match[0])
    return render(request, 'match/home.html')


# matches people from the group identified by pk
def match_group(request, pk):  
    group_in = Group.objects.get(id=pk)
    if request.user == group_in.owner:

        # add admin to the group
        group_in.members.add(request.user.Profile)
        print('here')
        # will delete all the old Pairs when running a new matching
        pairs = Pair.objects.all().filter(pair_group=group_in)
        for pair in pairs:
            print('delete here')
            pair.delete()

        member_list = [Group.members.all() for Group in Group.objects.all().filter(id=pk)]
        group_users = [Profile.user for Profile in member_list[0]]

        if len(group_users) == 1:
            messages.warning(request, f'You\'re the only person in this group. A matching cannot be run on one person.')
            return redirect('group-detail', pk)


        print('group users')
        print(group_users)

        matching = full_match(group_users)
        for match in matching:
            print('make here')
            user1, user2 = User.objects.get(id=match[0].id), User.objects.get(id=match[1].id)
            pair = Pair(pair_1=user1.id, pair_1_first=user1.first_name, pair_1_last=user1.last_name,
                        pair_2=user2.id, pair_2_first=user2.first_name, pair_2_last=user2.last_name,
                        pair_group=group_in, pair1_email=user1.email, pair2_email=user2.email,
                        pair1_image=user1.Profile.image, pair2_image=user2.Profile.image,
                        pair1_pMessage=user1.Profile.personal_message, pair2_pMessage=user2.Profile.personal_message)
            pair.save()

        # context = {
        #     'pairs': Pair.objects.all().filter()
        # }

        return redirect('group-detail', pk)
    else:
        return redirect('group-detail', pk)


# matching function
def full_match(users):
    
    # get preference/no preference user lists
    pref_users = [user for user in users if user.Profile.prefs_match==True]
    rand_users = [user for user in users if user not in pref_users]
    
    # call helper functions
    pref_matching_even, pref_remainder = pref_match_helper(pref_users)
    rand_matching_even, rand_remainder = rand_match_helper(rand_users)

    # edge case handling
    if len(pref_remainder) == 0 and len(rand_remainder) == 0: 
        return pref_matching_even + rand_matching_even
    
    elif len(pref_remainder) == 1 and len(rand_remainder) == 0: 
        odd_user = pref_remainder[0]
        users.remove(odd_user)
        other_user = random.choice(users)
        return pref_matching_even + rand_matching_even + [[odd_user, other_user]]
    
    elif len(pref_remainder) == 0 and len(rand_remainder) == 1: 
        odd_user = rand_remainder[0]
        users.remove(odd_user)
        other_user = random.choice(users)
        return pref_matching_even + rand_matching_even + [[odd_user, other_user]]
    
    else:
        new_match = [pref_remainder[0], rand_remainder[0]]
        return pref_matching_even + rand_matching_even + [new_match]


# random matching helper function
def rand_match_helper(users):

    # if there are 0 users
    if len(users) == 0: return [], []
    
    # shuffle users
    random.shuffle(users)
    
    # separate users into even #, remainder
    highest_even = (len(users) // 2) * 2
    users_even = users[:highest_even]
    users_remainder = users[highest_even:]
    
    # get matching
    matching = get_match(users_even)

    return matching, users_remainder


# preference-based matching helper function
def pref_match_helper(users):
    
    # separate users into even #, remainder
    random.shuffle(users)
    highest_even = (len(users) // 2) * 2
    users_even = users[:highest_even]
    users_remainder = users[highest_even:]

    # if users_even is empty
    if len(users_even) == 0: return [], users_remainder

    # preferences to use for current matching
    curr_prefs = np.random.permutation(5)
    
    # fetch user preferences
    preferences = {}
    for user in users_even: preferences[user.id] = fetch_prefs(user, curr_prefs)
    
    # get all permutations of users
    perms = list(permutations(users_even))

    # variables for minimum-dist matching
    min_dist = 1000000
    min_matching = []

    # iterate over permutations of users, find minimum-dist matching
    for perm in perms:
        perm = list(perm)
        matching = get_match(perm)
        distance = get_match_dist(matching, preferences)
        if distance < min_dist: min_matching, min_dist = matching, distance
    
    return min_matching, users_remainder


# sets user 2 as user 1 match
def set_match(user1, user2):

    user1.Profile.mate_ID = user2.id
    user1.Profile.mate_firstname = user2.first_name
    user1.Profile.mate_lastname = user2.last_name
    user1.Profile.mate_personal_message = user2.Profile.personal_message
    user1.Profile.mate_image = user2.Profile.image
    user1.Profile.mate_email = user2.email
    user1.Profile.is_matched = True
    user1.Profile.save()


# fetches user preferences
def fetch_prefs(user, curr_prefs):

    prefs = np.zeros(10)
    prefs[0] = user.Prefs.pref1
    prefs[1] = user.Prefs.pref2
    prefs[2] = user.Prefs.pref3
    prefs[3] = user.Prefs.pref4
    prefs[4] = user.Prefs.pref5
    prefs[5] = user.Prefs.pref6
    prefs[6] = user.Prefs.pref7
    prefs[7] = user.Prefs.pref8
    prefs[8] = user.Prefs.pref9
    prefs[9] = user.Prefs.pref10
    
    return prefs[curr_prefs]


# fetches matching for given ordering of users
def get_match(user_list):
    
    # set up matching list
    matching = []

    # add pairs
    i, numUsers = 0, len(user_list)
    while i < numUsers - 1:
        matching.append([user_list[i], user_list[i + 1]])
        i += 2

    return matching


# get average distance between pairs in matching
def get_match_dist(matching, prefs):

    matching_dist = 0
    for match in matching:
        pref1, pref2 = prefs[match[0].id], prefs[match[1].id]
        match_dist = np.linalg.norm(pref2 - pref1)**2
        matching_dist += match_dist

    return matching_dist/len(matching)











# # matches people from the group identified by pk
# def match_group(request, pk):  
#     group_in = Group.objects.get(id=pk)
#     if request.user == group_in.owner:

#         # will delete all the old Pairs when running a new matching
#         pairs = Pair.objects.all().filter(pair_group=group_in)
#         for pair in pairs:
#             pair.delete()

#         is_group = True

#         matching = random_match(is_group, pk)
#         for match in matching:
#             user1, user2 = User.objects.get(id=match[0]), User.objects.get(id=match[1])
#             pair = Pair(pair_1=user1.id, pair_1_first=user1.first_name, pair_1_last=user1.last_name,
#                         pair_2=user2.id, pair_2_first=user2.first_name, pair_2_last=user2.last_name, pair_group=group_in)
#             pair.save()

#         # context = {
#         #     'pairs': Pair.objects.all().filter()
#         # }

#         return redirect('group-detail', pk)
#     else:
#         return redirect('group-detail', pk)
