import requests


api_key = "Token 508711f53445fa67d8bdc1c97da256eacaef2e5e"
header_info = {'Authorization': api_key}
  # "Token dccec1ad173d2abaf88b542a02095f8d93ea97df",
  # "Token 8271c9035b3a113a16111392722a7bb4d9278a2c",
  # "Token 64936db353e36faa7ec880bb81331706cd4216a7"
timer = {'time': 0, 'purpose': 'move purposefully'}
room_info = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=header_info).json()

print(room_info['cooldown'])
