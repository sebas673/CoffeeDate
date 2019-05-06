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
        fields = ['pref1', 'pref2', 'pref3', 'pref4', 'pref5']

    q1 = 'This is question 1'
    q2 = 'This is question 2' 
    q3 = 'This is question 3' 
    q4 = 'This is question 4' 
    q5 = 'This is question 5'   

    pref1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q1)
    pref2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q2)
    pref3 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q3)
    pref4 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q4)
    pref5 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=q5)


class PrefsDetailView(DetailView):
    model = Prefs

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['pairs'] = Pair.objects.filter(pair_group=self.object)
    #     return context


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

        # will delete all the old Pairs when running a new matching
        pairs = Pair.objects.all().filter(pair_group=group_in)
        for pair in pairs:
            pair.delete()

        member_list = [Group.members.all() for Group in Group.objects.all().filter(id=pk)]
        group_users = [Profile.user for Profile in member_list[0]]

        matching = full_match(group_users)
        for match in matching:
            user1, user2 = User.objects.get(id=match[0].id), User.objects.get(id=match[1].id)
            pair = Pair(pair_1=user1.id, pair_1_first=user1.first_name, pair_1_last=user1.last_name,
                        pair_2=user2.id, pair_2_first=user2.first_name, pair_2_last=user2.last_name, pair_group=group_in)
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
    
    # do something with pref_remainder
    return pref_matching_even + rand_matching_even


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

    # if there are 0 users
    if len(users) == 0: return [], []
    
    # separate users into even #, remainder
    highest_even = (len(users) // 2) * 2
    users_even = users[:highest_even]
    users_remainder = users[highest_even:]
    
    # fetch user preferences
    preferences = {}
    for user in users_even: preferences[user.id] = fetch_prefs(user)
    
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
def fetch_prefs(user):

    prefs = np.zeros(5)
    prefs[0] = user.Prefs.pref1
    prefs[1] = user.Prefs.pref2
    prefs[2] = user.Prefs.pref3
    prefs[3] = user.Prefs.pref4
    prefs[4] = user.Prefs.pref5
    
    return prefs


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
