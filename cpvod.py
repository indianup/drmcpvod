import os
from services.drm_service import generate_drm_keys

# Load the token from environment variables
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', 'default_token_if_not_set')

url = input("url: ")

result = generate_drm_keys(url, ACCESS_TOKEN)
if "error" in result:
    print(f"Error: {result['error']}")
else:
    print(f"\nMPD URL: {result['mpd_url']}\n")
    for key in result['keys']:
        print(f"--key {key}")
