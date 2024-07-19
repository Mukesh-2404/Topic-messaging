from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from firebase_admin import messaging
from database.db import get_topics, log_notification

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/')
def index():
    return render_template('index.html')

@notifications_bp.route('/get_topics')
def get_topics_route():
    topics = get_topics()
    return jsonify(topics)

@notifications_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('notifications.index'))

@notifications_bp.route('/send_notification', methods=['POST'])
def send_notification():
    try:
        title = request.form['title']
        message_body = request.form['message']
        topic_name = request.form['topic']

        if not title or not message_body or not topic_name:
            return jsonify({"success": False, "error": "Title, message, and topic are required"}), 400

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=message_body,
            ),
            topic=topic_name,
        )

        response = messaging.send(message)
        print(f'Successfully sent message to topic {topic_name}: {response}')

        # function call for storing into database
        log_notification(topic_name, title, message_body)

        return jsonify({"success": True, "response": response})
    except Exception as e:
        print(f'Error sending message: {e}')
        return jsonify({"success": False, "error": str(e)}), 500