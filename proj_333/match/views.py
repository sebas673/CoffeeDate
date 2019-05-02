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

    pref1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    pref2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    pref3 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    pref4 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    pref5 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


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
    is_group = False
    pk = -1

    matching = random_match(is_group, pk)
    for match in matching:
        user1, user2 = User.objects.get(id=match[0]), User.objects.get(id=match[1])
        set_match(user1, user2)
    return render(request, 'match/home.html')


# matches people from the group identified by pk
def match_group(request, pk):  
    group_in = Group.objects.get(id=pk)
    if request.user == group_in.owner:

        # will delete all the old Pairs when running a new matching
        pairs = Pair.objects.all().filter(pair_group=group_in)
        for pair in pairs:
            pair.delete()

        is_group = True

        matching = random_match(is_group, pk)
        for match in matching:
            user1, user2 = User.objects.get(id=match[0]), User.objects.get(id=match[1])
            pair = Pair(pair_1=user1.id, pair_1_first=user1.first_name, pair_1_last=user1.last_name,
                        pair_2=user2.id, pair_2_first=user2.first_name, pair_2_last=user2.last_name, pair_group=group_in)
            pair.save()

        # context = {
        #     'pairs': Pair.objects.all().filter()
        # }

        return redirect('group-detail', pk)
    else:
        return redirect('group-detail', pk)


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


# if is_group is True then match all the members of the group with pk
def random_match(is_group, pk):  
    pairs = []

    if is_group == False:
        user_ids = [user.id for user in User.objects.all().filter(Profile__is_matched='False')]

    elif is_group == True:
        member_list = [Group.members.all() for Group in Group.objects.all().filter(id=pk)]
        user_ids = [Profile.user.id for Profile in member_list[0]]

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
