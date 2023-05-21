
import requests, time, json

# filler
port = 5000

user_id = None
user_pin = None

package = {}
def update_package(object_name, pos_rot_tuple):
    global package

    if object_name not in package:
        package[object_name] = {}

    package[object_name]["position"] = pos_rot_tuple[0]
    package[object_name]["rotation"] = pos_rot_tuple[1]

    response = requests.put('http://connorpersonal.space:5002/vr/cache', data={'user_id': str(user_id), 'pin': str(user_pin), 'data': json.dumps(package)})
    if response.status_code != 200:
        print("Error: " + str(response.status_code))
        print(response.text)

#data = {"Hello World": ":)"}

# post
#response = requests.post('http://connorpersonal.space:5002/vr/cache', data={'user_id': 'test', 'pin': '1234', 'data': json.dumps(data)})
#print(response.json())

# get
#response = requests.get('http://connorpersonal.space:5002/vr/cache', params={'user_id': 'test', 'pin': '1234'})
#print(response.json())


# filler
def run_server():
    pass

# filler
def stop_server():
    pass