from PIL import Image
import os

CONST_NEW_WIDTH = 200
CONST_NEW_HEIGHT = 200

RUTA = r"hats & shoes"
NEW_FOLDER = f"{RUTA}_{CONST_NEW_WIDTH}x{CONST_NEW_HEIGHT}"

def resize(ruta, new_route):
    try:
        img = Image.open(ruta)
    except:
        return

    if (not img):
        return

    width, height = img.size

    new_width = CONST_NEW_WIDTH
    new_height = CONST_NEW_HEIGHT

    if width > height:
        aspect_ratio =  height / width
        new_width = CONST_NEW_WIDTH
        new_height = int(new_width * aspect_ratio)
    else:
        aspect_ratio = width / height
        new_height = CONST_NEW_HEIGHT
        new_width = int(new_height * aspect_ratio)
    # print(f"RESIZED: {width}x{height}px -> {new_width}x{new_height}px")

    img = img.resize( (new_width, new_height) )
    img.save(new_route)
    # img.show()
    
# resize(RUTA)

os.mkdir(NEW_FOLDER)
for folder in os.scandir(RUTA):    
    new_cloth_folder = f"{NEW_FOLDER}/{folder.name}/"
    os.mkdir(new_cloth_folder)
    subfolder_route = f"{RUTA}/{folder.name}"
    print(folder.name)
    for img in os.scandir(subfolder_route):
        full_route = f"{subfolder_route}/{img.name}"
        new_full_route = f"{NEW_FOLDER}/{folder.name}/{img.name}"
        resize(full_route, new_full_route)
    