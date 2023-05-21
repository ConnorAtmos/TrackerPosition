import requests, time

#######################################################################################
# How to use this file
#######################################################################################
# This file just has one function that gets the user id of a roblox user.
# To use this file, import it into your own file like this:
# import roblox_user_id
#######################################################################################

#######################################################################################
# Steps in main.py:
#######################################################################################
# 1. Import roblox_user_id.py
# ex:
# import roblox_user_id
#
# 2. Get the user id
# ex:
# user_id = roblox_user_id.get_user_id("mrfrogg1")
#
# user_id should be 20504526
#######################################################################################


def get_user_id(username, attempts=0):
    r = requests.get("https://users.roblox.com/v1/users/search?keyword=" + username + "&limit=10")
    r = r.json()

    if 'errors' in r and r['errors'][0]['message'] != '':
        print("Error: " + r['errors'][0]['message'])

        # retry 5 times
        if attempts < 5:
            time_s = 3**(attempts+1)
            print("Retrying in " + str(time_s) + " seconds")
            time.sleep(time_s)
            return get_user_id(username, attempts + 1)
        return None

    if len(r["data"]) == 0:
        print("Error: No users found")
        return None

    return r["data"][0]["id"]
