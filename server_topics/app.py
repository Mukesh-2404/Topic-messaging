from flask import Flask
from config import db_config

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'morususfsdgfsd'  

# Import routes
from routers.notifications import notifications_bp

app.register_blueprint(notifications_bp)

if __name__ == '__main__':
    app.run(debug=True)
 