import mysql.connector
from config import db_config
from datetime import datetime
import pytz

def get_topics():
    conn = None
    topics = []
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT topic_name FROM Topics")  
        topics = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return [topic[0] for topic in topics]

def log_notification(topic_name, title, message_body):
    conn = None
    try:
        # GMT time 
        gmt = pytz.timezone('GMT')
        now = datetime.now(gmt)
        
        # GMT to IST convrsion
        ist = pytz.timezone('Asia/Kolkata')
        ist_now = now.astimezone(ist)
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO TopicsLogs (topic_name, title, messageBody, timestamp) VALUES (%s, %s, %s, %s)",
            (topic_name, title, message_body, ist_now)
        )
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()