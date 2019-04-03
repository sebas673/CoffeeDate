import numpy as np


# function that returns matching in form: 
# [[student 1, student 2], [student 3, student 4] ... ]
def matching(num_users):
  
  # edge cases
  if num_users < 2: return False # REPLACE WITH EXCEPTION
  if num_users == 2: return [[0, 1]]
  
  pairs = []
  users = np.arange(num_users)
  
  while len(users) > 1:
    users, pair = pick_rand_pair(users)
    pairs.append(pair)
  
  # odd # of users case
  if len(users) == 1:
    dd_user = np.random.permutation([user for user in range(num_users) if user != users[0]])[0]
    pairs.append([dd_user, users[0]])
  
  return pairs


# function that picks 2 random people from those remaining
def pick_rand_pair(users):
  
  pair = np.random.permutation(users)[:2].tolist()
  users = np.asarray([user for user in users if user not in pair])
  
  return users, pair