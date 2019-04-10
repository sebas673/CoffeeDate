from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import Profile 
import random
# handles the traffic from the homepage. Takes in a request arg and
# returns what we want the user to see when they are sent to this route.


def home(request):
    return render(request, 'match/home.html')

def matchAlgorithm(request):
    matching = random_match()
    for match in matching:
        user1, user2 = User.objects.get(id=match[0]), User.objects.get(id=match[1])
        set_match(user1, user2)
    return render(request, 'users/profile.html', {'title': 'matchAlgorithm'})

def set_match(user1, user2):
    user1.profile.matchedMateID = user2.id
    user1.profile.matchedMatePName = user2.profile.preferred_name
    user1.profile.matchedMatePMessage = user2.profile.personal_message
    user1.profile.matchedMateImage = user2.profile.image
    user1.profile.matchedMatePEmail = user2.email
    user1.profile.save()

    user2.profile.matchedMateID = user1.id
    user2.profile.matchedMatePName = user1.profile.preferred_name
    user2.profile.matchedMatePMessage = user1.profile.personal_message
    user2.profile.matchedMateImage = user1.profile.image
    user2.profile.matchedMatePEmail = user1.email
    user2.profile.save()


def random_match():

  pairs = []
  user_ids = [user.id for user in User.objects.all()]

  random.shuffle(user_ids)
 
  i = 0
  j = 0
  numUsers = len(user_ids)
  while i < numUsers - 1:
      pairs.append([user_ids[i], user_ids[i+1]])
      i+=2

  # odd # of users case                                                                                       
  if numUsers % 2 == 1: pairs.append([user_ids[0], user_ids[numUsers-1]])

  return pairs