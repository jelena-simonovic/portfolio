from main import app, db
from app.models import User

with app.app_context():
    db.create_all()
    new_user = User(id=1, username='admin') 
    new_user.set_password('admin123')  # Use the set_password method to hash the password
    db.session.add(new_user)
    db.session.commit()
    print("User created successfully.")