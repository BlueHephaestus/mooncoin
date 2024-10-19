"""
Import the phase data, create all the other entries, save it to our lookup file.



We need, for every day:
    - Moon phase #, which we can use to convert to:
    - - name of moon phase, e.g. "Waning Crescent"
    - - emoji
    - - image, etc.

0 – new moon
0-0.25 – waxing crescent
0.25 – first quarter
0.25-0.5 – waxing gibbous
0.5 – full moon
0.5-0.75 – waning gibbous
0.75 – last quarter
0.75 -1 – waning crescent

For each day:
file: 0.png, 0.45.png, etc.
desc: "New Moon 🌑" etc.

We convert their number to an image we can reference in the imgs folder.
"""
import json
import requests
import os

with open("moon_data.json", "r") as f:
    moon_data = json.load(f)

# Final lookup table to populate.
lookup = {}

icons = sorted(os.listdir("imgs"), key=lambda x: int(x.split(".")[0]))

def get_moon_data(mp):
    """

    :param mp:
    :return: [icon, banner, desc, illumination %]
    RETURNS THE VALUE THAT IS ASSOCIATED WITH THIS IN THE LOOKUP TABLE
    Icon, banner, desc, illumination %
    
    Reminder:
    
    0 – new moon
    0-0.25 – waxing crescent
    0.25 – first quarter
    0.25-0.5 – waxing gibbous
    0.5 – full moon
    0.5-0.75 – waning gibbous
    0.75 – last quarter
    0.75 -1 – waning crescent
    """

    # Get illumination %
    if mp <= 0.5:
        ill = 2*mp
    else:
        ill = 2*(1-mp)

    ill = int(ill*100)


    intervals = [0] + [i/16 for i in range(1,16)]
    def get_nearest_icon(mp,icon_i):
        if icon_i in [2, 6, 10, 14]:
            d = lambda x, y: abs(x - y)
            dists = [d(mp, intervals[icon_i - 1]), d(mp, intervals[icon_i]), d(mp, intervals[icon_i + 1])]

            # Get closest icon using our intervals
            # Minimum distance from the 3 values at this point (will not be a special moon)
            icon_i_offset = dists.index(min(dists))-1 # so if we get 1, we know to keep it as icon_i originally was.

            icon = icons[icon_i+icon_i_offset]
            icon_i = icon_i + icon_i_offset
        else:
            # Special moon
            icon = icons[icon_i]
        return icon_i, icon


    # Get desc and icon index
    if mp == 0:
        desc = "New Moon 🌑"
        emoji = "🌑"
        icon_i = 0
    elif 0 < mp < 0.25:
        desc = "Waxing Crescent 🌒"
        emoji = "🌒"
        icon_i = 2
    elif mp == 0.25:
        desc = "First Quarter 🌓"
        emoji = "🌓"
        icon_i = 4
    elif 0.25 < mp < 0.5:
        desc = "Waxing Gibbous 🌔"
        emoji = "🌔"
        icon_i = 6
    elif mp == 0.5:
        desc = "Full Moon 🌕"
        emoji = "🌕"
        icon_i = 8
    elif 0.5 < mp < 0.75:
        desc = "Waning Gibbous 🌖"
        emoji = "🌖"
        icon_i = 10
    elif mp == 0.75:
        desc = "Last Quarter 🌗"
        emoji = "🌗"
        icon_i = 12
    else:# 0.75 < mp < 1.0
        desc = "Waning Crescent 🌘"
        emoji = "🌘"
        icon_i = 14

    """
    Can now update the icon_i to a more granular one if it's in the in-betweens.
    For instance, we might have 0.01 mp but we'd want this to be set to 1.png, not 2.png.
    Since these will by default be the following indices (in-betweens):
        2,6,10,14
    We can just apply it to those.
    I could do the modulo but why bother
    """
    icon_i, icon = get_nearest_icon(mp, icon_i)

    banner = None # not doing this for now.

    desc = f"{desc}, {ill}% Illumination"

    # Return icon, banner, desc

    return icon, banner, emoji, desc

    # print(f"{mp}, {desc}, {ill}%")


# mp = moon phase
cycles = []
cyc = []

for date, mp in moon_data.items():
    if mp == 0:
        # Eval last cycle
        # Start new one
        cycles.append(cyc)
        cyc = []
        cyc.append([date,mp])
    else:
        cyc.append([date,mp])

# Cycles is now list of lists, each list inside is a cycle, in order of time.
NM = 0.0
FQ = 0.25
FM = 0.5
LQ = 0.75

def get_nearest_moon(cycle, M):
    # cycle = [(date, mp), ...]
    # get closest by distance
    closest_i = cycle.index(min(cycle, key=lambda x: abs(x-M)))
    return closest_i


# First one is incomplete, ignore
for cycle_i, cycle in enumerate(cycles[1:]):
    # Now we can clean up per cycle! (thankfully there is always a 0.0, it seems)
    # Make sure each cycle has at least one of the special moons - NM, FQ, FM, LQ
    # if cycle.count(NM) == 0:
    #     closest_i = get_nearest_moon(cycle, NM)
    #     cycles[cycle_i][closest_i][1] = NM
    # if cycle.count(FQ) == 0:
    #     closest_i = get_nearest_moon(cycle, FQ)
    #     cycles[cycle_i][closest_i][1] = FQ
    # if cycle.count(FM) == 0:
    #     closest_i = get_nearest_moon(cycle, FM)
    #     cycles[cycle_i][closest_i][1] = FM
    # if cycle.count(LQ) == 0:
    #     closest_i = get_nearest_moon(cycle, LQ)
    #     cycles[cycle_i][closest_i][1] = LQ
    dates,cycle = zip(*cycle)
    dates = list(dates)
    cycle = list(cycle)
    a = [cycle.count(NM),cycle.count(FQ), cycle.count(FM),cycle.count(LQ)]
    for moon in [NM, FQ, FM, LQ]:
        if cycle.count(moon) == 0:
            closest_i = get_nearest_moon(cycle, moon)
            cycle[closest_i] = moon # Set it in our ref



    # Remove any duplicates of the special moons, remove the first instances and replace them with close to that number.
    # I'm assuming there won't be 3 but if there were, this still works good enough for me.
    for moon in [NM, FQ, FM, LQ]:
        while cycle.count(moon) > 1:
            cycle[cycle.index(moon)] -= 0.01

    # Update the main list now that we've done this
    cycles[cycle_i] = list(zip(dates,cycle))


# Now we have all our cycles in order, flatten the list again and get our metadata for each.
# We can now get the metadata for each moon phase, and save it to our lookup table.
data = []
for cycle in cycles:
    data += cycle

lookup = {}
for date, mp in data:
    lookup[date] = get_moon_data(mp)
    print(date, lookup[date])

# Save this to a file
with open("lookup.json", "w") as f:
    json.dump(lookup, f, ensure_ascii=False, indent=4)




"""
Go through them by cycle, get each section that's 0 -> next 0.
"""