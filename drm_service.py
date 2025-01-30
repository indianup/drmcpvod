import requests
from bs4 import BeautifulSoup
from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH
from utils.wvd_check import wvd_check

def generate_drm_keys(video_url, access_token):
    try:
        wvd = wvd_check()

        headers = {
            'x-access-token': access_token
        }

        response = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={video_url}', headers=headers).json()

        if response.get('status') != 'ok':
            return {"error": "Failed to fetch DRM URLs"}

        mpd = response['drmUrls']['manifestUrl']
        lic = response['drmUrls']['licenseUrl']
        mpd_response = requests.get(mpd)
        soup = BeautifulSoup(mpd_response.text, 'xml')

        uuid = soup.find('ContentProtection', attrs={'schemeIdUri': 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed'})
        if not uuid:
            return {"error": "PSSH data not found in MPD"}
        
        pssh = uuid.find('cenc:pssh').text
        ipssh = PSSH(pssh)
        device = Device.load(wvd)
        cdm = Cdm.from_device(device)
        session_id = cdm.open()
        challenge = cdm.get_license_challenge(session_id, ipssh)
        licence = requests.post(lic, data=challenge, headers=headers)
        licence.raise_for_status()

        cdm.parse_license(session_id, licence.content)

        keys = []
        for key in cdm.get_keys(session_id):
            if key.type != 'SIGNING':
                keys.append(f'{key.kid.hex}:{key.key.hex()}')

        cdm.close(session_id)

        return {"mpd_url": mpd, "keys": keys}
    except Exception as e:
        return {"error": str(e)}
