from flask import Flask
from flask_migrate import Migrate
from routes import hospital_routes
from models import db
from seed import seed_data  # Import seed_data function

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Register the hospital_routes Blueprint
app.register_blueprint(hospital_routes)

# Route for the default landing page
@app.route('/')
def index():
    return 'Welcome to the MediFinder application!'

if __name__ == '__main__':
    # Create the tables (if not already created) and seed the data
    with app.app_context():
        db.create_all()
        seed_data()

    app.run(debug=True)
