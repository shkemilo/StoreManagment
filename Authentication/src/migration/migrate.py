from time import sleep
from flask import Flask
from commons.configuration import Configuration
from flask_migrate import Migrate, init, migrate, upgrade
from commons.models import database, Role, UserRole, User
from sqlalchemy_utils import database_exists, create_database

application = Flask(__name__)
application.config.from_object(Configuration)

migrateObject = Migrate(application, database)

done = False

while (not done):
    try:
        if (not database_exists(application.config["SQLALCHEMY_DATABASE_URI"])):
            create_database(application.config["SQLALCHEMY_DATABASE_URI"])

        print("Migrations starting")

        database.init_app(application)

        with application.app_context() as context:
            init()
            migrate(message="Production migration")
            upgrade()

            adminRole = Role(name="admin")
            userRole = Role(name="user")

            database.session.add(adminRole)
            database.session.add(userRole)
            database.session.commit()

            admin = User(
                email="admin@admin.com",
                password="1",
                forename="admin",
                surname="admin"
            )

            database.session.add(admin)
            database.session.commit()

            userRole = UserRole(
                userId=admin.id,
                roleId=adminRole.id
            )

            print("Migrations Finished")

            done = True
    except Exception as error:
        print(error)
        sleep(1)
