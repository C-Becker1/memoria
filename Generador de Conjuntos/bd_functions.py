from shutil import copyfile

import os

import mysql.connector
from mysql.connector import Error

from decouple import config

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

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
    
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

HOST_NAME = config("HOST_NAME")
USER_NAME = config("USER_NAME")
USER_PASSWORD = config("USER_PASSWORD")
DB_NAME = config("DB_NAME")

connection = create_server_connection(HOST_NAME, USER_NAME, USER_PASSWORD, DB_NAME)

ROUTE = "img"
NEW_ROUTE = "sv_img"

CreateFolder(".", NEW_ROUTE)

def OnlyRequiredFiles():
    query = "SELECT r.ID, r.ID_Cloth, IMG_Route FROM rel_cloth_outfit AS r INNER JOIN cloth ON cloth.ID = r.ID_Cloth"
    result = read_query(connection, query) 
    unique_clothes = set()
    for id, id_cloth, img_route in result:
        if id_cloth not in unique_clothes:
            CopyImageToNewFolder( f"{ROUTE}/{img_route}", f"{NEW_ROUTE}/{img_route}" )
            unique_clothes.add( id_cloth )

# OnlyRequiredFiles()


