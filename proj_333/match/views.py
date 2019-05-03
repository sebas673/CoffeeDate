from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import Profile 
import random
# handles the traffic from the homepage. Takes in a request arg and
# returns what we want the user to see when they are sent to this route.


def home(request):
    return render(request, 'match/home.html')


# Old matching algorithm (replaced by find_match_rand below)
def matchAlgorithm(request):
    matching = random_match()
    for match in matching:
        user1, user2 = User.objects.get(id=match[0]), User.objects.get(id=match[1])
        set_match(user1, user2)
    return render(request, 'users/profile.html', {'title': 'matchAlgorithm'})


# FUNCTIONS FOR RANDOM MATCHING (STAND ALONE) -----------------------------------------------------
# This function is an updated version of the one above that matches people randomly. We don't
# want to use this though - we want to use find_match below. 

# request handler
def find_match_rand(request):
    users = [user for user in User.objects.all().filter(Profile__is_matched='False')] # Profile needs to change to Prefs?
    matching = rand_match_helper(users)
    for match in matching:
        set_match(match[0], match[1])
        set_match(match[1], match[0])
    return render(request, 'match/home.html')


# FUNCTIONS FOR FULL MATCHING (PREFERENCE-BASED + RANDOM) -----------------------------------------
# Functions that handle matching based on preferences (or no preferences).
# IMPORTANT: Currently don't handle any edge cases! But should work for any even number of users
# above 2.

# request handler
def find_match(request):
    users = [user for user in User.objects.all().filter(Profile__is_matched='False')] # Profile needs to change to Prefs?
    matching = full_match(users)
    for match in matching:
        set_match(match[0], match[1])
        set_match(match[1], match[0])
    return render(request, 'match/home.html')


# matching function
def full_match(users):
    
    # get preference/no preference user lists
    pref_users = [user for user in users if user.has_preferences==True]
    rand_users = [user for user in users if user not in pref_users]
    
    # call helper functions
    pref_matching_even, pref_remainder = pref_match_helper(pref_users)
    rand_matching_even, rand_remainder = rand_match_helper(rand_users)
    
    return pref_matching_even + rand_matching_even


# HELPER FUNCTIONS --------------------------------------------------------------------------------


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


# sets user 2 as user 1's match
def set_match(user1, user2):

    user1.Prefs.mate_ID = user2.id
    user1.Prefs.mate_firstname = user2.first_name
    user1.Prefs.mate_lastname = user2.last_name
    user1.Prefs.mate_personal_message = user2.Prefs.personal_message
    user1.Prefs.mate_image = user2.Prefs.image
    user1.Prefs.mate_email = user2.email
    user1.Prefs.is_matched = True
    user1.Prefs.save()


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