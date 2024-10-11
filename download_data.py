"""
Get all the data so we have it saved, including the moon events.

Makes use of my usual strategy of getting API keys,
    then cycling through them each time to avoid rate limiting.
    as well as testing them initially.
"""
import json

import requests
MOON_API_KEYS = [
    "6X6AN44CEB6825G9TBEL9H235",
    "3SDVZNVLW5EJQBE6MZ7QMT3WQ",
    "CMQ8N7SN9FBHRMXSDKK86GYYN",
    "W8RDKBHTHK3UV7MWNRZPAHQNW",
    "7JWQMV9WC5JJBUQF22L83ERCB",
    "2VPJ28CTFE8EW6RTBK8PULF4Y",

    "4VC9QTHSPFXW5L2F2VXUZJLWR",
    "XC52BDVEMRZ36XS9CU6G782P4",
    "8N7VE7DU57F4PZWVAGHNN5ZVK",
    "U8XMTFZLWN2Y59MYJMERZGT6U",
    "UB7HSQJ56P9RUPG56M8PFDFB3",
    
    "5PMLT687G7E4UUPDFWHGBS65E",
    "ZMV9HEXU664HPKVSRNLB93LQE",
    "KZWGYHQU6JZUJ6VTKLAUDH68W",
    "RHK7VYYRZXLYRWCCNR94GGRDW",
    "4TL5LFAY3PFAMN97VCTQRXQHR",
    
    "JSN83SWW77989S6ZE43SESMX2",
    "8ARQXLV9DNE3GQ7GVP6TVCC87",
    "Z3RK8ACQE7B4YJFZ9AEPWPQ4D",
]

TEST_API_KEYS = True
MOON_API_KEY = MOON_API_KEYS[0]
MOON_BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Sacramento,CA/{date1}/{date2}"
MOON_BASE_HEADERS = {
    'accept': 'application/json',
}
# Location is by default 51.5, 0, which is Greenwich, England (UTC)
# So it's also where UTC timezone is,
# So we can use this as a default location for moon data.
MOON_BASE_PARAMS = {
    "key": MOON_API_KEY,
    "include": "days",
    "elements": "datetime,moonphase,sunrise,sunset,moonrise,moonset",
}
def next_api_key():
    global MOON_API_KEY
    MOON_API_KEY = MOON_API_KEYS[(MOON_API_KEYS.index(MOON_API_KEY) + 1) % len(MOON_API_KEYS)]
    MOON_BASE_PARAMS["key"] = MOON_API_KEY
    return MOON_API_KEY
# Test API keys to make sure they still work and remove if any dont before we do anything
_n = len(MOON_API_KEYS)
if TEST_API_KEYS:
    to_rm = []
    for i, key in enumerate(MOON_API_KEYS):
        # Do sample request with each to check if they are still valid

        MOON_BASE_PARAMS["key"] = key
        response = requests.get(MOON_BASE_URL.format(date1="2024-10-01", date2="2024-10-02"), headers=MOON_BASE_HEADERS, params=MOON_BASE_PARAMS, timeout=20)
        if response.status_code != 200:
            print(f"API key {i+1}/{_n}: {key} is invalid with status code {response.status_code}, removing...")
            to_rm.append(key)
            continue
        print(f"API key {i+1}/{_n}: {key} is valid")

    for key in to_rm:
        MOON_API_KEYS.remove(key)
    print(f"Removed {len(to_rm)} invalid API keys")
MOON_API_KEY = MOON_API_KEYS[0]

def moon_api_req(date1, date2):
    try:
        retries = 5
        while retries > 0:
            response = requests.get(MOON_BASE_URL.format(date1=date1, date2=date2), headers=MOON_BASE_HEADERS, params=MOON_BASE_PARAMS, timeout=20)
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
from pprint import pprint as pp

# Get moon phases for every day from 2024 to 3024, to be used for computing all the other data.
data = {}
try:
    for year in range(2028, 2031):
        date1 = f"{year}-01-01"
        date2 = f"{year+1}-01-01"
        print(f"Getting moon data for {year}")
        res = moon_api_req(date1, date2)
        for day in res["days"]:
            data[day["datetime"]] = day["moonphase"]
except:
    with open("moon_data.json", "w") as f:
        json.dump(data, f, indent=4)
with open("moon_data.json", "w") as f:
    json.dump(data, f, indent=4)

# print(pp(moon_api_req("2024-11-01", "2024-12-01")))
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
