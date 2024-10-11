"""
Get all the data so we have it saved, including the moon events.

Makes use of my usual strategy of getting API keys,
    then cycling through them each time to avoid rate limiting.
    as well as testing them initially.

"""
import requests
MOON_API_KEYS = [
    "fb17a5b661mshd65f0506b9963c2p1e4e6djsn1174d5435dae",
    "e1748088ddmshf67ba4347bdd975p1a8de2jsn0a545e552fd2",
    "0824a2c382mshb6a7ecac1677e76p11250cjsndc3ea1d6ec95",
    "bcee4fa275mshb865add344610cfp1a8b66jsn19dbcd9162be",
    "6c925f5fc2msh9b0d7fdec48e8a5p1e3e99jsndb79e168c058",
    "3f09df65abmsh594a95d23859fc1p1d0677jsnd338105525a6",
]
TEST_API_KEYS = True
API_KEY_HEADER = 'X-Rapidapi-Key'
MOON_API_KEY = MOON_API_KEYS[0]
MOON_BASE_URL = "https://moon-phase.p.rapidapi.com/{}"
MOON_BASE_HEADERS = {
    'accept': 'application/json',
    API_KEY_HEADER: MOON_API_KEY,
}
# Location is by default 51.5, 0, which is Greenwich, England (UTC)
# So it's also where UTC timezone is,
# So we can use this as a default location for moon data.
MOON_BASE_PARAMS = {
    "filters": "moon"
}
def next_api_key():
    global MOON_API_KEY
    MOON_API_KEY = MOON_API_KEYS[(MOON_API_KEYS.index(MOON_API_KEY) + 1) % len(MOON_API_KEYS)]
    MOON_BASE_HEADERS[API_KEY_HEADER] = MOON_API_KEY
    return MOON_API_KEY
# Test API keys to make sure they still work and remove if any dont before we do anything
_n = len(MOON_API_KEYS)
if TEST_API_KEYS:
    to_rm = []
    for i, key in enumerate(MOON_API_KEYS):
        # Do sample request with each to check if they are still valid
        endpoint = "advanced"

        MOON_BASE_HEADERS[API_KEY_HEADER] = key
        response = requests.get(MOON_BASE_URL.format(endpoint), headers=MOON_BASE_HEADERS, timeout=20)
        if response.status_code != 200:
            print(f"API key {i+1}/{_n}: {key} is invalid with status code {response.status_code}, removing...")
            to_rm.append(key)
            continue
        print(f"API key {i+1}/{_n}: {key} is valid")

    for key in to_rm:
        MOON_API_KEYS.remove(key)
    print(f"Removed {len(to_rm)} invalid API keys")


def moonapi_req(endpoint, params):
    try:
        retries = 5
        while retries > 0:
            response = requests.get(MOON_BASE_URL.format(endpoint), headers=MOON_BASE_HEADERS, params=params,
                                    timeout=999)
            data = response.json()
            if response.status_code == 429:
                # retries exceeded, go next API key
                next_api_key()
                continue
            elif response.status_code != 200 or len(data) == 0 or data is None:
                # Some error, retry
                # if response.status_code in [401, 403]:
                #     # Unauthorized, go next API key
                #     next_api_key()
                #     continue
                next_api_key()
                retries -= 1
                continue
            next_api_key()
            return data

    except:
        return None

"""
Example Response
{
    "moon": {
        "phase": 0.9772280089784628,
        "phase_name": "Waning Crescent",
        "stage": "waning",
        "illumination": "1%",
        "age_days": 29,
        "lunar_cycle": "97.72%",
        "emoji": "🌘",
        "zodiac": {
            "sun_sign": "Libra",
            "moon_sign": "Virgo"
        },
        "moonrise": "05:24",
        "moonrise_timestamp": 1727839440,
        "moonset": "18:16",
        "moonset_timestamp": 1727885760,
        "moon_altitude": -35.455969713637046,
        "moon_distance": 405853.65547797695,
        "moon_azimuth": 336.5507109048147,
        "moon_parallactic_angle": 14.343661714114937,
        "next_lunar_eclipse": {
            "timestamp": 1741931996,
            "datestamp": "Fri, 14 Mar 2025 06:59:56 +0100",
            "type": "Total Lunar Eclipse",
            "visibility_regions": "Pacific, Americas, western Europe, western Africa"
        }
    }
}
"""
"""
# Data we want.
{
    "moon": {
        "phase": 0.9772280089784628,
        "phase_name": "Waning Crescent",
        "stage": "waning",
        "illumination": "1%",
        "age_days": 29,
        "lunar_cycle": "97.72%",
        "emoji": "🌘",
        "zodiac": {
            "sun_sign": "Libra",
            "moon_sign": "Virgo"
        },
        "moonrise": "05:24",
        "moonrise_timestamp": 1727839440,
        "moonset": "18:16",
        "moonset_timestamp": 1727885760,
        "moon_altitude": -35.455969713637046,
        "moon_distance": 405853.65547797695,
        "moon_azimuth": 336.5507109048147,
        "moon_parallactic_angle": 14.343661714114937,
        "next_lunar_eclipse": {
            "timestamp": 1741931996,
            "datestamp": "Fri, 14 Mar 2025 06:59:56 +0100",
            "type": "Total Lunar Eclipse",
            "visibility_regions": "Pacific, Americas, western Europe, western Africa"
        }
    }
}
"""
