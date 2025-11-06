import psycopg2
from psycopg2 import errors
from decimal import Decimal
import datetime

def connect():
    #connecting to postgres and to my database 'Fitness'
    database_connection = psycopg2.connect(
        host="localhost",
        user="postgres",
        database= "Fitness",
        password="###",
    )

    #setting up connections
    return database_connection.cursor(), database_connection 

def cleanUp(cursor, database_connection):
    cursor.close()
    database_connection.close()


def login(user, email):
    cursor, database_connection = connect()
    cursor.execute("Select email from Members")
    member_emails = [row[0] for row in cursor.fetchall()]
    if email in member_emails and user == "member":
        cursor.execute("Select member_id from Members where email = %s", (email,))
        member_id = [row[0] for row in cursor.fetchall()]
        cursor.execute("Select name from Members where email = %s", (email,))
        name = [row[0] for row in cursor.fetchall()]
        return name, user, member_id, email
    
    cursor.execute("Select email from Trainers")
    trainer_emails = [row[0] for row in cursor.fetchall()]
    if email in trainer_emails and user == "trainer":
        cursor.execute("Select trainer_id from Trainers where email = %s", (email,))
        trainer_id = [row[0] for row in cursor.fetchall()]
        cursor.execute("Select name from Trainers where email = %s", (email,))
        name = [row[0] for row in cursor.fetchall()]
        return name, user, trainer_id, email

    cursor.execute("Select email from AdministrativeStaff")
    staff_emails = [row[0] for row in cursor.fetchall()]
    if email in staff_emails and user == "staff":
        cursor.execute("Select staff_id from AdministrativeStaff where email = %s", (email,))
        staff_id = [row[0] for row in cursor.fetchall()]
        cursor.execute("Select name from AdministrativeStaff where email = %s", (email,))
        name = [row[0] for row in cursor.fetchall()]
        return name, user, staff_id, email
    
    cleanUp(cursor, database_connection)
    return ['User does not exist'], "Error", "Error", "Error"

#creating a new member (account creation)
def createMember(name, gender, email, phone, fitness_goal):
    cursor, database_connection = connect()
    cursor.execute("""INSERT INTO Members (name, gender, email, phone, fitness_goal) VALUES (%s, %s, %s, %s, %s)""",
                   (name, gender, email, phone, fitness_goal))
    database_connection.commit()
    cleanUp(cursor, database_connection)

#updating account details
def updatePersonalDetails(name, gender, email, phone, fitness_goal):
    cursor, database_connection = connect()
    cursor.execute("""UPDATE Members SET name = %s, gender = %s, email = %s, phone = %s, fitness_goal = %s WHERE email = %s""",
                   (name, gender, email, phone, fitness_goal, email))
    database_connection.commit()
    cleanUp(cursor, database_connection)

def getGoal(member_id):
    cursor, database_connection = connect()
    cursor.execute("Select fitness_goal from Members where member_id=%s", (member_id,))
    row = cursor.fetchone()
    cleanUp(cursor, database_connection)
    return row_to_dict(cursor, row)

#creating a new healthmetric for a member
def createNewHealthMetric(member_id, date_recorded, height, weight, heart_rate, body_fat_percentage):
    cursor, database_connection = connect()
    cursor.execute("""INSERT INTO HealthMetrics (member_id, date_recorded, height, weight, heart_rate, body_fat_percentage) VALUES (%s, %s, %s, %s, %s, %s)""",
                   (member_id, date_recorded, height, weight, heart_rate, body_fat_percentage))
    database_connection.commit()
    cleanUp(cursor, database_connection)

#getting history of metrics
def getMetrics(member_id):
    cursor, database_connection = connect()
    cursor.execute("Select * from HealthMetrics where member_id=%s", (member_id,))
    metrics = cursor.fetchall()

    cleanUp(cursor, database_connection)
    return [row_to_dict(cursor, row) for row in metrics]
    

#book training session
def bookTrainingSession(member_id, room_id, trainer_id, staff_id, session_date, start_time, end_time, status):
    cursor, database_connection = connect()
    try:
        cursor.execute("""INSERT INTO PersonalTrainingSessions (member_id, room_id, trainer_id, staff_id, session_date, start_time, end_time, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (member_id, room_id, trainer_id, staff_id,session_date, start_time, end_time, status))
        
        database_connection.commit()
        return None
    except Exception as e:
        pg_error = str(e)

        return pg_error 
    finally:
        cleanUp(cursor, database_connection)

#edit training session
def editTrainingSession(member_id, room_id, trainer_id, staff_id, session_date, start_time, end_time, status, session_id):
    cursor, database_connection = connect()
    try:
        cursor.execute("""UPDATE PersonalTrainingSessions SET member_id = %s, room_id = %s, trainer_id = %s, staff_id = %s, session_date = %s, start_time = %s, end_time = %s, status = %s WHERE member_id = %s""",
                    (member_id, room_id, trainer_id, staff_id, session_date, start_time, end_time, status, session_id))
        database_connection.commit()
        return None
    except Exception as e:
        pg_error = str(e)

        return pg_error 
    finally:
        cleanUp(cursor, database_connection)

#get all training sessions
def getAllTrainingSession():
    cursor, database_connection = connect()
    cursor.execute("""SELECT * from PersonalTrainingSessions""")
    
    assigned_sessions = cursor.fetchall()
    cleanUp(cursor, database_connection)
    return [row_to_dict(cursor, row) for row in assigned_sessions] 

#view training sessions
def getTrainingSessions(member_id):
    cursor, database_connection = connect()
    cursor.execute("""SELECT 
                r.room_name, 
                t.name AS trainer_name, 
                pts.session_date, 
                pts.start_time, 
                pts.end_time, 
                pts.status
            FROM PersonalTrainingSessions pts
            JOIN Rooms r ON pts.room_id = r.room_id
            JOIN Trainers t ON pts.trainer_id = t.trainer_id
            WHERE pts.member_id = %s
            ORDER BY pts.session_date, pts.start_time;""", (member_id,))
    
    assigned_sessions = cursor.fetchall()
    cleanUp(cursor, database_connection)
    return [row_to_dict(cursor, row) for row in assigned_sessions]


#view assigned training sessions
def assignedTrainingSessions(trainer_id):
    cursor, database_connection = connect()
    cursor.execute("""SELECT 
                r.room_name, 
                m.name AS member_name, 
                pts.session_date, 
                pts.start_time, 
                pts.end_time, 
                pts.status
            FROM PersonalTrainingSessions pts
            JOIN Rooms r ON pts.room_id = r.room_id
            JOIN Members m ON pts.member_id = m.member_id
            WHERE pts.trainer_id = %s
            ORDER BY pts.session_date, pts.start_time;""", (trainer_id,))
    
    assigned_sessions = cursor.fetchall()
    cleanUp(cursor, database_connection)
    return [row_to_dict(cursor, row) for row in assigned_sessions]

#search members
def searchMember(name):
    cursor, database_connection = connect()
    cursor.execute("Select * from Members as m INNER JOIN LatestMemberMetrics as l ON m.member_id = l.member_id where l.name=%s", (name,))
    members = cursor.fetchall()

    cleanUp(cursor, database_connection)
    return [row_to_dict(cursor, row) for row in members]

#view last metric of members using view
def viewLastMetric(member_id):
    cursor, database_connection = connect()
    cursor.execute("Select * from LatestMemberMetrics where member_id=%s", (member_id,))
    row = cursor.fetchone()
    cleanUp(cursor, database_connection)
    return row_to_dict(cursor, row)

#assign a room to a session
def assignRoom(session_id, room_id, staff_id):
    cursor, database_connection = connect()
    cursor.execute("""UPDATE PersonalTrainingSessions SET room_id = %s, staff_id = %s WHERE session_id = %s""", 
                   (room_id, staff_id, session_id))

    database_connection.commit()
    cleanUp(cursor, database_connection)

def getRooms():
    cursor, database_connection = connect()
    cursor.execute("Select * from Rooms")
    members = cursor.fetchall()

    cleanUp(cursor, database_connection)
    return [row_to_dict(cursor, row) for row in members]

def getMembers():
    cursor, database_connection = connect()
    cursor.execute("Select * from Members")
    members = cursor.fetchall()

    cleanUp(cursor, database_connection)
    return [row_to_dict(cursor, row) for row in members]

def getTrainers():
    cursor, database_connection = connect()
    cursor.execute("Select * from Trainers")
    members = cursor.fetchall()

    cleanUp(cursor, database_connection)
    return [row_to_dict(cursor, row) for row in members]

#helper function
def row_to_dict(cursor, row):

    if row is None:
        return None

    columns = [desc[0] for desc in cursor.description]

    row_dict = dict(zip(columns, row))

    for key, value in row_dict.items():
        if isinstance(value, Decimal):
            row_dict[key] = float(value)
        elif isinstance(value, datetime.date):
            row_dict[key] = value.strftime("%Y-%m-%d")

    return row_dict
"""
def main():
   
    

if __name__ == "__main__":
    main()
"""

