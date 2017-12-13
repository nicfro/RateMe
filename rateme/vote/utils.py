import pyodbc
import datetime
from passlib.context import CryptContext
from random import randint

DRIVER = "ODBC Driver 13 for SQL Server"
DRIVER = "unixODBC-devel"


def connection():
    return cnxn = pyodbc.connect("""
            Driver={%s};
            Server=tcp:rateme.database.windows.net,1433;
            Database=RateMe;
            Uid=Nicolai@rateme;
            Pwd={Hejmor1!};
            Encrypt=yes;
            TrustServerCertificate=no;
            Connection Timeout=30;
            """ % (DRIVER)
                      )


cursor = None #cnxn.cursor()

'''
Create user in database
'''


def CreateNewUser(username, password, country, email, gender, birthYear):
    cursor.execute("""
                    SELECT 1
                    FROM [dbo].[Users]
                    WHERE Username = ?
                   """, [username])
    userExists = cursor.rowcount != 0
    if userExists:
        return "User already exists"
    else:
        myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])
        salt = str(randint(1, 200000))
        hash1 = myctx.hash(password + salt)

        Username = username.lower()
        HashedPwd = hash1
        PwdSalt = salt
        Country = country
        Email = email
        Gender = gender
        BirthYear = birthYear
        cursor.execute("""
            INSERT INTO [dbo].[Users]
                   ([Username]
                   ,[HashedPwd]
                   ,[PwdSalt]
                   ,[Country]
                   ,[Email]
                   ,[Gender]
                   ,[BirthYear])
             VALUES
                   (?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?)
        """, [Username, HashedPwd, PwdSalt, Country, Email, Gender, BirthYear])
        cnxn.commit()


'''
Login Function
'''


def login(username, password):
    cursor.execute("""
    SELECT [HashedPwd]
          ,[PwdSalt]
    FROM [dbo].[Users]
    WHERE Username = ?
    """, username)

    resp = cursor.fetchone()

    hash1 = resp[0]
    salt = resp[1]
    return myctx.verify(password + salt, hash1)


'''
Writes reports to the database
'''


def reportImage(username, ImagePath):
    cursor.execute("""
        INSERT INTO [dbo].[Report]
                   ([Username]
                   ,[ImagePath])
             VALUES
                   (?,
                    ?)
    """, [Username, ImagePath])
    cnxn.commit()


'''
Calculating new elo scores
'''


def updateScore(winner, loser, tie, k):
    EA = (1 / (1 + 10 ** ((loser - winner) / 400)))
    EB = (1 / (1 + 10 ** ((winner - loser) / 400)))

    if tie == 0:
        winner = winner + k * (1 - EA)
        loser = loser + k * (0 - EB)
    else:
        winner = winner + k * (0.5 - EA)
        loser = loser + k * (0.5 - EB)

    return winner, loser


'''
Fills in the vote table in the database
Calls the update elo function in the end
'''


def vote(username, imagepath1, imagepath2, result):
    cursor.execute("""
            INSERT INTO [dbo].[Vote]
                   ([Username]
                   ,[imagePath1]
                   ,[imagePath2]
                   ,[Result])
             VALUES
                   (?,
                    ?,
                    ?,
                    ?)
        """, [username, imagepath1, imagepath2, result])
    cnxn.commit()

    updateElo(imagepath1, imagepath2, result)


'''
Writes the vote to the elo table
Updates the Elo in the image table
'''


def updateElo(imagepath1, imagepath2, result):
    if results == "image1":
        winner = imagepath1
        loser = imagepath2
        tie = 0
        imagepath1Elo, imagepath2Elo = updateScore(winner, loser, tie, 30)
    elif results == "image2":
        winner = imagepath2
        loser = imagepath1
        tie = 0
        imagepath2Elo, imagepath1Elo = updateScore(winner, loser, tie, 30)
    elif results == "tie":
        winner = imagepath1
        loser = imagepath2
        tie = 1
        imagepath1Elo, imagepath2Elo = updateScore(winner, loser, tie, 30)

    post1 = [[imagepath1, imagepath1Elo], [imagepath2, imagepath2Elo]]
    cursor.executemany("""
            INSERT INTO [dbo].[Elo]
                   ([IimagePath]
                   ,[EloScore])
             VALUES
                   (?,
                    ?)
        """, post1)
    cnxn.commit()

    post2 = [[imagepath1Elo, imagepath1], [imagepath2Elo, imagepath2]]
    cursor.executemany("""
            UPDATE [dbo].[Images]
               SET [EloScore] = ?
             WHERE [ImagePath] = ?
        """, post2)
    cnxn.commit()


'''
Updates the image table in the database
'''


def uploadImage(ImagePath, Username, GenderOfImage):
    cursor.execute("""
        INSERT INTO [dbo].[Images]
               ([ImagePath]
               ,[Username]
               ,[EloScore]
               ,[GenderOfImage])
         VALUES
               (?,
                ?,
                ?,
                ?)
    """, [ImagePath, Username, 1500, GenderOfImage])
    cnxn.commit()
