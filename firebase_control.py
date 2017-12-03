
from firebase import firebase
fb = firebase.FirebaseApplication('https://gal-9000.firebaseio.com/', None)

def fb_put(a, b, c):
    fb.put(a, b, c)