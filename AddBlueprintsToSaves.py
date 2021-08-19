import xml.etree.ElementTree as ET
import re
import random

startingBlueprints = [0,1,6,9,14,20,22,36,50]
allNonStartingBlueprints = [x for x in range (51) if x not in startingBlueprints]
smallMunitionsBlueprints = [31, 32, 33, 34, 35, 45, 46, 48]
largeMunitionsBlueprints = [15, 16, 17, 18, 19, 29, 30, 37, 38, 39, 40]
turretBlueprints = [10, 11, 12, 13, 26, 27, 28, 47, 49]
utilityBlueprints = [23, 24, 25, 41, 42, 43, 44]
sufaceChassisBlueprints = [2, 3]
airChassisBlueprints = [4, 5, 7]

facilitiesAndBlueprints = {
    1 : smallMunitionsBlueprints,
    2 : largeMunitionsBlueprints,
    3 : turretBlueprints,
    4 : utilityBlueprints,
    5 : sufaceChassisBlueprints,
    6 : airChassisBlueprints
}

turretAmmoPairings = {
    11 : 30,
    30 : 11, # Rocket pod and rockets
    12 : 32,
    32 : 12, # CIWS and 20mm
    13 : 17,
    17 : 13, # IR Missile Turret
    26 : 31,
    31 : 26, # Flare launcher and flare
    27 : 33,
    33 : 27, # Battle cannon and 100mm
    28 : 34,
    34 : 28, # Artillery Gun and 120mm
    47 : 48,
    48 : 47 # 40mm turret and 40mm
}

def getRandomBlueprintFromType(facilityType):
    return random.choice(facilitiesAndBlueprints[facilityType])


def addBlueprintNode(elem, newBlueprintId):
    bpUnlocks = elem.find("blueprint_unlocks")
    # print ("Trying to unlock: " + str(newBlueprintId))
    alreadyPresent = [int(x.get("value")) for x in bpUnlocks.findall("b")]
    # print ("Already present: " + str(alreadyPresent))
    # avoid pointless duplication - should we reroll?
    if (newBlueprintId not in alreadyPresent):
        child = ET.SubElement(bpUnlocks, 'b')
        child.set('value', str(newBlueprintId))
        # print ("No duplicates, added")
        return True # success, no duplicates
    # print("Duplicate detected, blueprint not added")
    return False # failure, nothing added, because duplicates

# load a save file

# can't load it raw as it has multiple top level nodes which is invalid xml.  Fake it by adding our own root node.
with open("save.xml") as f:
    xml = f.read()
root = ET.fromstring(re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xml) + "</root>")

# find the tiles section
tiles = root.findall("./scene/tiles/tiles/t")

# foreach tiles
for t in tiles:
    # production islands only
    facilityType = int(t.find("facility").get('category'))
    if not (facilityType >= 1 and facilityType <= 6):
        continue

    # empty islands need blueprints
    blueprintCount = len(t.findall("./blueprint_unlocks/*"))
    if (blueprintCount == 0):
        # add a blueprint of the appropriate type
        newBlueprint = getRandomBlueprintFromType(facilityType)

        print("Empty Island: Since it has facility type " + str(facilityType) + ", adding blueprint " + str(newBlueprint))

        #create the new XML node for the save file
        addBlueprintNode(t, newBlueprint)

    # tough islands deserve extra
    # +1 extra blueprint for a 3 shield island,
    # +2 extra blueprints for a 4 shield island or above
    # So islands between 0.30 and 0.45 get +1, and islands above 0.45 get 2 extra
    islandDifficulty = float(t.get('difficulty_factor'))
    bonusBlueprintCount = 0
    if (islandDifficulty >= 0.30 and islandDifficulty < 0.45):
        print("Difficulty 3 island, gets 1 extra blueprint chances")
        bonusBlueprintCount = 1
    elif (islandDifficulty >= 0.45):
        print("Difficulty 4+ island, gets 2 extra blueprint chances")
        bonusBlueprintCount = 2

    for i in range(bonusBlueprintCount):
        noDuplicates = True
        # while add blueprint node returns false (because duplicates found) try again until you get to 10 then just add
        # a completely random blueprint instead of a from type
        for j in range(10):
            newBlueprint = getRandomBlueprintFromType(facilityType)
            noDuplicates = addBlueprintNode(t, newBlueprint)
            if noDuplicates:
                print("Since it has facility type " + str(facilityType) + ", added typed blueprint " + str(newBlueprint))
                break
        if (noDuplicates == False):
            newBlueprint = random.choice(allNonStartingBlueprints)
            print("Failed to add typed blueprint, attempting to add random blueprint " + str(newBlueprint))
            addBlueprintNode(t, newBlueprint)

    # match turrets and ammo
    for existingBlueprintEntry in t.findall("blueprint_unlocks/*"):
        existingBlueprintId = int(existingBlueprintEntry.get('value'))
        if (existingBlueprintId in turretAmmoPairings.keys()):
            print("Found half of a pair!")
            # get the matching half
            otherHalf = turretAmmoPairings[existingBlueprintId]
            print ("Since island had blueprint " + str(existingBlueprintId) + ", adding " + str(otherHalf))
            #insert another node
            addBlueprintNode(t, otherHalf)

tree = ET.ElementTree(root)
tree.write('moddedsave.xml')

# Somewhat hackily reload the output and remove the root node we added earlier.
with open("moddedsave.xml") as f2:
    text = f2.read()

rejiggedText = re.sub("<root>", "<?xml version=\"1.0\" encoding=\"UTF-8\"?>", text)
rejiggedText = re.sub("</root>", "", rejiggedText)

with open("moddedsave.xml", "w") as f3:
    f3.write(rejiggedText)
