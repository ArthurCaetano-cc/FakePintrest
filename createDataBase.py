
from fakePintrest import database, app
from fakePintrest.models import User, Photo

with app.app_context():
    database.create_all()