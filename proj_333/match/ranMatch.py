from django.contrib.auth.models import User
import random

# function that returns matching in form:                                                                     

# [[student 1, student 2], [student 3, student 4] ... ]                                                       

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

a = random_match()
print(a)