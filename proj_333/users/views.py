from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from uniauth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from match.models import Pair, Group


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.Profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            # updates the fields of the matched mate as well
            user_that_updated = request.user
            if user_that_updated.Profile.is_matched == True:
                user_to_update = User.objects.all().get(Profile__mate_ID=user_that_updated.id)
                user_to_update.Profile.mate_firstname = user_that_updated.first_name
                user_to_update.Profile.mate_lastname = user_that_updated.last_name
                user_to_update.Profile.mate_image = user_that_updated.Profile.image
                user_to_update.Profile.mate_personal_message = user_that_updated.Profile.personal_message
                user_to_update.Profile.save()

                # updates the fields of the pair as well
                pairs = Pair.objects.all().filter(pair_1=user_that_updated.id)
                for pair in pairs:
                    pair.pair_1_first = user_that_updated.first_name
                    pair.pair_1_last = user_that_updated.last_name
                    pair.save()

                pairs = Pair.objects.all().filter(pair_2=user_that_updated.id)
                for pair in pairs:
                    pair.pair_2_first = user_that_updated.first_name
                    pair.pair_2_last = user_that_updated.last_name
                    pair.save()

            messages.info(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.Profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
