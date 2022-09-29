import smtplib, ssl
from email.message import EmailMessage

from random import randint

import mysql.connector
from mysql.connector import Error

MAX_PASSWORD_LENGTH = 10

# LOCAL HOST CREDENTIALS
HOST_NAME = "localhost"
USER_NAME = "root"
DB_NAME = "memoria"
USER_PASSWORD = "admin"


# Receptores
"""
SEND_MAILS_TO = [
    "elpadrinosrg@gmail.com",
    "rojasguerrasebastian@gmail.com",
    "sebastian.rojasgue@sansano.usm.cl",
    "fabio.pazos99@gmail.com",
    "almendra.soza@sansano.usm.cl",
    "camilo.farah@sansano.usm.cl",
    "pia.gonzalez@sansano.usm.cl",
    "tiaremendez04@gmail.com ",
    "lelicer@fen.uchile.cl",
    "rorrodrigo.-@hotmail.com",
    "valentina.mendoza@sansano.usm.cl",
    "bernabe.garcia@sansano.usm.cl",
    "simon.montenegro@usach.cl"
]

SEND_MAILS_TO = [
    "mmejiasvaras@gmail.com", "maria.canoles.r@usach.cl"
]

"""

SEND_MAILS_TO = [
    "danielsilva@ug.uchile.cl",
    "sixto.morales@ug.uchile.cl",
    "vicente.vera@alumnos.ucentral.cl",
    "natalia.arancibia.pizarro@gmail.com",
    "magdalena.vasquez@mail.udp.cl"
]

def generatePassword(passwordLength):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    
    newPassword = ""
    
    for i in range(passwordLength):
        isDigit = randint(0, 1) == 0 # si el número aleatorio es 0, entonces el siguiente caracter generado corresponde a un dígito
        if (isDigit):
            randomChar = digits[ randint(0, len(digits) - 1) ]
        else:
            randomChar = alphabet[ randint(0, len(alphabet) - 1) ]
            isLowerCase = randint(0, 1) == 0
            if (isLowerCase):
                randomChar = randomChar.lower()

        newPassword += randomChar
    return newPassword

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

def InsertIntoUserTable( user, password, name ):
    query = f"INSERT INTO user (Username, Password, Name) VALUES ('{user}', '{password}', '{name}')" 
    execute_query(connection, query)
    return



# query = "SELECT * FROM user"
connection = create_server_connection(HOST_NAME, USER_NAME, USER_PASSWORD, DB_NAME)
# result = read_query(connection, query)






# Configuration
smtp_server = "smtp.gmail.com"
port = 465  # For starttls

# Login to mail
sender_email = "mail-bot@sebastian-rg.com"
password = "wooyvqkdmrrejyoj" #app password
password = ".Ww5M5gaW)D5"
# receiver_email = "elpadrinosrg@gmail.com"

def SendMail(mail, username, password, name):
    msg = EmailMessage()

    mailBody = f"""
        Hola, {name}!
        Se ha registrado su cuenta en la plataforma de recolección de datos para el trabajo
        de memoria de Sebastián. Sus datos de ingreso se presentan a continuación.

        Nombre de usuario: {username}
        Contraseña: {password}

        Puede acceder a la plataforma mediante el siguiente enlace:
            https://sebastian-rg.com

        Se solicita porfavor, anotar su contraseña en algún lugar, pues ésta es generada de
        manera aleatoria y no puede ser modificada. En caso de olvido o extravío, comunicarse con
        el administrador. 

        Este es un mensaje generado automáticamente. El que responde es weón yera.
    """

    msg.set_content(mailBody)

    msg['Subject'] = f"[Notificación] Creación de Cuenta"
    msg['From'] = sender_email
    msg['To'] = mail

    server.send_message(msg)


# server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server = smtplib.SMTP_SSL("mail.sebastian-rg.com", 465)
server.ehlo()
server.starttls
server.login(sender_email, password)

for mail in SEND_MAILS_TO:
    username = mail.split("@")[0]
    name = username.replace(".", " ")
    password = generatePassword(MAX_PASSWORD_LENGTH)
    InsertIntoUserTable(username, password, name)
    SendMail(mail, username, password, name)

server.quit()



