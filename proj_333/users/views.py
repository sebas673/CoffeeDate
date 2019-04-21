from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from uniauth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User


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
                user_to_update.Profile.mate_personal_message = user_that_updated.Profile.personal_message
                user_to_update.Profile.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.Profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
