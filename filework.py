import shutil, os


def addZeroDigit(name):
    dashIndex = name.rfind("-")
    dotIndex = name.rfind(".")
    #if there is only one number to the name
    if  dashIndex+2 == dotIndex:
        return name[:dashIndex+1] + "0" + name[dashIndex+1:]
    else:
        return None

def addZeroDigitDir(root):
    fileList = os.listdir(root)
    replacementMap = {}
    for name in fileList:
        newName = addZeroDigit(name)
        if newName is not None:
            replacementMap[name] = newName
    return replacementMap

def simpleNameFix(name, replacementMap):
    changed = False
    for strToReplace in replacementMap.keys():
        if (name.find(strToReplace) != -1):
            changed = True
            startName = name[:name.find(strToReplace)]
            endName = name[name.find(strToReplace) + len(strToReplace):]
            name =  startName + replacementMap[strToReplace] + endName
    if changed:
        return name
    else:
        return None

def simpleDirFixNameMap(root, replacementMap):
    fileList = os.listdir(root)
    newNames = {}
    episodeNum = 1
    for name in fileList:
        newName = simpleNameFix(name, replacementMap)
        if newName is not None:
            newNames[name] = newName
    return newNames

def makeNewName(name, seasonNum, strToReplaceList, episodeNum):
    for strToReplace in strToReplaceList:
        if (name.rfind(strToReplace) != -1):
            startName = name[:name.rfind(strToReplace)]
            endName = name[name.rfind(strToReplace) + len(strToReplace):]
            episodeStr = str(episodeNum).zfill(2)
            toAddToName = " - s" + str(seasonNum).zfill(2) + "e" + episodeStr + " - "
            return startName + toAddToName + endName
    return None


def makeNewNameMap (root, seasonNum, strToReplaceList):
    fileList = os.listdir(root)
    fileList.remove(".DS_Store")
    newNames = {}
    episodeNum = 1
    for name in fileList:
        newName = makeNewName(name, seasonNum, strToReplaceList, episodeNum)
        if newName is not None:
            newNames[name] = newName
            episodeNum += 1
    return newNames


def renameFromMap(dir, nameMap):
    for oldName in nameMap.keys():
        #print (dir+oldName, ":", dir+nameMap[oldName])
        os.rename(dir+oldName, dir+nameMap[oldName])


def main():
    seasonNumber = 1
    dir = "/Volumes/DragonMedia/1-video/1-tv/"+str(seasonNumber)+"/"
    map = simpleDirFixNameMap(dir, {"":""})
    print(len(map))
    for oldName in map.keys():
        print(oldName, ":", map[oldName])
    check = input("okay to make simple fixes?")
    if check == "yes":
        renameFromMap(dir, map)

    # finalMap = addZeroDigitDir(dir)
    # print(len(finalMap))
    # for oldName in finalMap.keys():
    #     print(oldName, ":", finalMap[oldName])
    # check = input("okay to make final name changes?")
    # if check == "yes":
    #     renameFromMap(dir, finalMap)

    finalMap = makeNewNameMap(dir,  seasonNumber, ["_"] )#+str(seasonNumber)+""])
    print(len(finalMap))
    for oldName in finalMap.keys():
        print(oldName, ":", finalMap[oldName])
    check = input("okay to make final name changes?")
    if check == "yes":
        renameFromMap(dir, finalMap)



main()

# print(makeNewNameMap("/Volumes/DragonMedia/1-video/1-tv/1-Simpsons/06", 6, ["_S6_", "_SEASON6_"]))
