import random
from PIL import Image
import mysql.connector
from mysql.connector import Error

import bd_functions as bd

LIST_CATEGORY_CLOTH_FILEPATH = "./list_category_cloth.txt"
LIST_ATTR_CLOTH_FILEPATH = "./list_attr_cloth.txt"
LIST_ATTR_IMG_FILEPATH = "./list_attr_img.txt"

FULL_ROUTE = "./img/"


ATTRIBUTE_TYPE = {
    1: "DISEÑO", # floral, graphic, striped, embroidered, pleated, solid, lattice
    2: "LARGO DE MANGAS", # long sleeve, short sleeve, sleeveless
    3: "LARGO DE FALDA", # maxi length, mini length, no dress       # not sure abt this
    4: "TIPO DE CUELLO", # crew neckline, v neckline, square neckline, no neckline
    5: "MATERIAL", # denim, chiffon, cotton, leather, faux, knit
    6: "AJUSTE", # tight, loose, conventional
}
ATTRIBUTE_NAME = [
    "floral", "graphic", "striped", "embroidered", "pleated", "solid", "lattice",
    "long_sleeve", "short_sleeve", "sleeveless",
    "maxi_length", "mini_length", "no_dress",
    "crew_neckline", "v_neckline", "square_neckline", "no_neckline",
    "denim", "chiffon", "cotton", "leather", "faux", "knit",
    "tight", "loose", "conventional"
]

CLOTH_CATEGORY = [
    "HAT",
    "UPPER BODY",
    "LOWER BODY",
    "FULL BODY",
    "SHOES"
]

def getClothCategory_FromImgUrl(name):
    name = name.strip().split("/")[0]
    name = name.split("_")[-1]
    return name

def readFile(fileName):
    List = []

    f = open(fileName)
    i = 0
    for line in f:
        if i < 2:
            i += 1
            continue
        
        categoryName, categoryType = line.strip().split(",")
        try:
            categoryType = int( categoryType.strip() )
        except:
            categoryType = categoryType.strip()

        List.append( ( categoryName.strip() , categoryType ) )

    f.close()
    return List
 
# flag = true: La categoría es un nombre
# flag = true: La categoría es un número que la representa
def getCategorySublist(L, categories, flag = True):
    newL = []
    for d in L:
        if flag:
            for c in categories:
                if d['clothCategoryName'].lower() == c:
                        newL.append(d)
                        break
        else:
            if d['clothCategoryType'] == categories:
                newL.append(d)
    return newL

def loadFiles():
    categoryCloth = listToDict( readFile(LIST_CATEGORY_CLOTH_FILEPATH) )
    attrCloth = listToDict( readFile(LIST_ATTR_CLOTH_FILEPATH) )
    ImgData = extendImgInfo( readFile(LIST_ATTR_IMG_FILEPATH), categoryCloth )
    
    upperBodyList = getCategorySublist(ImgData, 1, False)   # obtener todos los registros upperBody
    lowerBodyList = getCategorySublist(ImgData, 2, False)   # obtener todos los registros lowerBody
    fullBodyList = getCategorySublist(ImgData, 3, False)   # obtener todos los registros fullBody

    terceraCapa = ["anorak", "bomber", "jacket", "parka", "peacoat", "poncho"]
    segundaCapa = ["blazer", "cardigan", "hoodie", "jersey", "sweater", "turtleneck", "flannel"]
    primeraCapa = ["blouse", "button-down", "halter", "henley", "tank", "tee", "top", "turtleneck", "flannel"]
    
    firstLayerList = getCategorySublist(ImgData, primeraCapa)
    secondLayerList = getCategorySublist(ImgData, segundaCapa)
    thirdLayerList = getCategorySublist(ImgData, terceraCapa)

    return attrCloth, ImgData, firstLayerList, secondLayerList, thirdLayerList, lowerBodyList

def extendImgInfo(L, category):
    newL = []

    columns = ", ".join(ATTRIBUTE_NAME)

    for route, attr in L:
        imgObject = {}
        newRoute = rreplace(route.split("/")[1], "-", "/",1)
        imgObject["route"] = newRoute
        clothCategory = getClothCategory_FromImgUrl(newRoute)
        imgObject["clothBodyPart"] = CLOTH_CATEGORY[category[clothCategory]]
        imgObject["clothCategoryName"] = clothCategory
        imgObject["clothCategoryType"] = category[clothCategory]
        Name = " ".join( route.split("/")[1].split("_")[0:-1] )
        imgObject["Name"] = Name
        attr = attr.split(" ")
        imgObject["attributes"] = attr
        newL.append(imgObject)

        values = ", ".join(attr)

        # Sección de código que permite subir cada registro a la tabla `cloth`.
        #   insertClothQuery = f"INSERT INTO cloth (Name, IMG_Route, ClothCategory, ClothCategoryName, {columns}) VALUES ('{Name}', '{newRoute}', '{CLOTH_CATEGORY[category[clothCategory]]}', '{clothCategory}', {values})"  
        #   execute_query(connection, insertClothQuery) 

    return newL

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

def listToDict(L):
    D = {}
    for key, val in L:
        D[key] = val
    return D

#función que se utiliza una vez para colocar una coma en los archivos y poder trabajarlos de mejor manera
def separateWithString(fileName, string = ","):
    lines = []
    f = open(fileName)
    i = 0
    for line in f:
        if i < 2:
            i += 1
            lines.append(line)
            continue

        line = line.strip().split(" ")
        line.insert(1, ",")
        line = " ".join(line) + "\n"

        lines.append(line)

    f.close()
    
    f = open(fileName, "w")
    for line in lines:
        f.write(line)
    f.close()

def getRandomBoolean():
    randInt = random.randint(0,1)
    return randInt == 0

def hasLayers():
    return getRandomBoolean(), getRandomBoolean()

def hasFullBody():
    return getRandomBoolean()

def hasHat():
    return getRandomBoolean()

def randomHat():
    return selectRandomFromList(hatList)

def randomFullBody():
    return selectRandomFromList(fullBodyList)

def randomFirstLayer():
    return selectRandomFromList(firstLayerList)

def randomSecondLayer():
    return selectRandomFromList(secondLayerList)

def randomThirdLayer():
    return selectRandomFromList(thirdLayerList)

def randomLowerbody():
    return selectRandomFromList(lowerBodyList)

def randomShoes():
    return selectRandomFromList(shoeList)

def selectRandomFromList(L):
    return L[random.randint(0, len(L)-1)]

def showOutfit(id, outfitSet):
    if id == 0:
        return False
    
    print(f"Displaying outfit with id = {id}")
    print(outfitSet[id])
    for cloth in outfitSet[id]:
        if cloth:
            print("ID:", cloth["Id"])
            print("Name:", cloth["Name"])
            print("Img Route:", cloth["ImgRoute"])
            print("Category:", cloth["Category"])
            print("Body Part:", cloth["Bodypart"])
            print("Atributes:", cloth["attrs"])

            image = Image.open(FULL_ROUTE + cloth["ImgRoute"])
            image.show()
    return True
    




"""
Anorak      ,   1 -> (3) Parca: Impermeable con capucha recubierto a menudo de piel natural o de imitación
Blazer      ,   1 -> (2) Chaqueta de vestir
Blouse      ,   1 -> (1) Blusa
Bomber      ,   1 -> (3)
Button-Down ,   1 -> (1) ??
Cardigan    ,   1 -> (2)
Flannel     ,   1 -> (1 o 2):  Es como una camisa a cuadrillé pero que se puede ocupar como segunda capa
Halter      ,   1 -> )1)
Henley      ,   1 -> (1)
Hoodie      ,   1 -> (2)
Jacket      ,   1 -> (3)
Jersey      ,   1 -> (2)
Parka       ,   1 -> (3)
Peacoat     ,   1 -> (3) 
Poncho      ,   1 -> (3)
Sweater     ,   1 -> (2)
Tank        ,   1 -> (1): Polera sin mangas
Tee         ,   1 -> (1)
Top         ,   1 -> (1)
Turtleneck  ,   1 (1 o 2)
"""







def insertClothIntoTable(cloth):
    columns = ", ".join(ATTRIBUTE_NAME)
    attrValues = ", ".join(cloth["list"])
    name = cloth["name"]
    img_route = cloth["img_route"]
    clothCategory = "SHOES"
    clothCategoryName = "Shoes"
    query = f"INSERT INTO cloth (Name, IMG_Route, ClothCategory, ClothCategoryName, {columns}) VALUES ('{name}', '{img_route}', '{clothCategory}', '{clothCategoryName}', {attrValues})"
    bd.execute_query(connection, query)
    # print(query)

def insertOutfitsIntoTable(_set):
    outfitId = 1
    for outfit in _set:
        outfitQuery = f"INSERT INTO outfit (ID, Name, Description) VALUES ({outfitId}, 'Vestimenta {outfitId}', 'Vestimenta {outfitId}')"
        bd.execute_query(connection, outfitQuery)
        for cloth in outfit:
            clothId = cloth["Id"]
            relClothOutfitQuery = f"INSERT INTO rel_cloth_outfit (ID_Outfit, ID_Cloth) VALUES ({outfitId}, {clothId})"
            bd.execute_query(connection, relClothOutfitQuery)
        outfitId += 1
    return True

def readCSVFile(nomarch):
    file = open(nomarch)
    firstLine = True
    retorno = []
    for line in file:
        
        if firstLine:
            firstLine = False
        else:
            line = line.strip().split(",")
            name = line[0]
            L = line[1:]
            imgRoute = getPath(name)
            obj = {
                "list": L,
                "name": name,
                "img_route": imgRoute}
            retorno.append(obj)
    return retorno

def getPath(name):
    name = "".join(name.split(" ")).lower()
    return f"shoes/{name}.jpg"

# connection = create_server_connection(HOST_NAME, USER_NAME, USER_PASSWORD, DB_NAME)

# r = readCSVFile("img/shoes/shoes_Attributes.csv")


def insertCloths(L):
    for obj in L:
        insertClothIntoTable(obj)


def loadClothes(ClothCategory = None, ClothCategoryName = None):
    _clothCategoryName = []
    results = []
    if ClothCategoryName:
        terceraCapa = ["anorak", "bomber", "jacket", "parka", "peacoat", "poncho"]
        segundaCapa = ["blazer", "cardigan", "hoodie", "jersey", "sweater", "turtleneck", "flannel"]
        primeraCapa = ["blouse", "button-down", "halter", "henley", "tank", "tee", "top", "turtleneck", "flannel"]
        if ClothCategoryName == "firstLayer":
            _clothCategoryName = primeraCapa
        elif ClothCategoryName == "secondLayer":
            _clothCategoryName = segundaCapa
        elif ClothCategoryName == "thirdLayer":
            _clothCategoryName = terceraCapa
        
        categories = ""
        for c in _clothCategoryName:
            categories += f"'{c}', "
        categories = categories[:-2] 
        query = f"SELECT * FROM cloth WHERE ClothCategoryName in ({categories})"
        results = bd.read_query(connection, query)
    if ClothCategory:
        query = f"SELECT * FROM cloth WHERE ClothCategory = '{ClothCategory}'"
        results = bd.read_query(connection, query)
    return results

# firstLayerList, secondLayerList, thirdLayerList, lowerBodyList = loadClothes()


def mapRegistersToObjects(L):
    newList = []
    for x in L:
        registro = {}

        clothId = x[0]
        clothName = x[1]
        clothDescription = x[2]
        clothIMG_Route = x[3]
        clothCategory = x[4]
        clothCategoryName = x[5]
        attrs = x[6:]
        i = 0
        attrsDict = {}
        for val in attrs:
            attrsDict[ATTRIBUTE_NAME[i]] = val
            i += 1

        registro['Id'] = clothId
        registro['Name'] = clothName
        registro['Description'] = clothDescription
        registro['ImgRoute'] = clothIMG_Route
        registro['Category'] = clothCategory
        registro['Bodypart'] = clothCategoryName
        registro['attrs'] = attrsDict
        
        newList.append(registro)
    
    return newList 

HOST_NAME = "localhost"
USER_NAME = "root"
DB_NAME = "memoria"
USER_PASSWORD = "admin"

connection = bd.create_server_connection(HOST_NAME, USER_NAME, USER_PASSWORD, DB_NAME)

firstLayerList = mapRegistersToObjects( loadClothes(ClothCategoryName = "firstLayer") )
# for x in firstLayerList:
    # print(x)
secondLayerList = mapRegistersToObjects( loadClothes(ClothCategoryName = "secondLayer") )
thirdLayerList = mapRegistersToObjects( loadClothes(ClothCategoryName = "thirdLayer") )
lowerBodyList = mapRegistersToObjects( loadClothes(ClothCategory = "LOWER BODY") )

shoeList = mapRegistersToObjects( loadClothes(ClothCategory = "SHOES"))
hatList = mapRegistersToObjects( loadClothes(ClothCategory = "HAT"))

# attrCloth, ImgData, firstLayerList, secondLayerList, thirdLayerList, lowerBodyList = loadFiles()
