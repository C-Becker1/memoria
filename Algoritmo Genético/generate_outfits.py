import mysql.connector
from mysql.connector import Error
from shutil import copyfile
import os
from datetime import datetime
import sys

def create_server_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def CopyImageToNewFolder(img_route, new_route):
    if (not os.path.exists(img_route)):
        return
    if (not os.path.exists(new_route)):
        CreateFolder(new_route.split("/")[0], new_route.split("/")[1])
    
    copyfile(img_route, new_route)
    return

def CreateFolder(route, foldername):
    folder_route = f"{route}/{foldername}"
    if (os.path.exists(folder_route)):
        return
    os.mkdir(folder_route)
    return  

def formatDate(string):
    date_list = string.split("-")
    formato = ["d", "M", "A", "H", "m"]
    new_string = ""
    for i in range(len(formato)):
        new_string += formato[i] + date_list[i]
        if i == 2:
            new_string += "_"
        else:
            new_string += "-"
    
    return new_string[:-1]   


weather_category = sys.argv[1]
modelo = sys.argv[2]
diversity_control = sys.argv[3]

nombre_carpeta = f"{modelo}_{diversity_control}"
# folder_name = f"{}C{weather_category}_{current_datetime}"
CreateFolder("./Solutions", nombre_carpeta)
CreateFolder(f"./Solutions/{nombre_carpeta}", f"C{weather_category}")



HOST_NAME = "localhost"
USER_NAME = "root"
DB_NAME = "memoria"
USER_PASSWORD = "admin"

connection = create_server_connection(HOST_NAME, USER_NAME, USER_PASSWORD, DB_NAME)


RUTA_BASE = "../Generador de Conjuntos/sv_img/"

now = datetime.now()
current_datetime = formatDate(now.strftime("%d-%m-%Y-%H-%M"))

solutions_file = "finalSolutions.txt" 

file = open(solutions_file)

read_record_query = "SELECT Name, IMG_Route, ID FROM cloth WHERE ID = {}"
i = 1
isFirstLine = True
for line in file:
    if isFirstLine:
        isFirstLine = False
        columns = line.strip().split(",")
        # weather_category = columns[-1]
    else:

        ids_ropa = line.strip().split(" ")[:6]

        other_folder_name = f"solution_{i}"
        CreateFolder(f"./Solutions/{nombre_carpeta}/C{weather_category}/", other_folder_name)

        for id in ids_ropa:
            result = read_query(connection, read_record_query.format(id))
            if len(result) != 0:
                img_name = result[0][0].replace("-img", "")
                CopyImageToNewFolder(f"{RUTA_BASE}/{result[0][1]}", f"./Solutions/{nombre_carpeta}/C{weather_category}/{other_folder_name}/{id}_{img_name}.jpg")
            print(result)
        i += 1
        # if i == 6:
            # break
file.close()

logs_file = "logs.txt"
diversity_file = "diversity_vs_generation.txt"

for file in [solutions_file, logs_file, diversity_file]:
    CopyImageToNewFolder(file, f"./Solutions/{nombre_carpeta}/C{weather_category}/{file}")
    os.remove(file)



        