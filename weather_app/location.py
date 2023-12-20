import geocoder
g = geocoder.ip('me')
def user():
    return g.latlng
