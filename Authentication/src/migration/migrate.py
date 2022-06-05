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
            customerRole = Role(name="customer")
            workerRole = Role(name="worker")

            database.session.add(adminRole)
            database.session.add(customerRole)
            database.session.add(workerRole)
            database.session.commit()

            print("Added roles")

            admin = User(
                email="admin@admin.com",
                password="1",
                forename="admin",
                surname="admin"
            )

            database.session.add(admin)
            database.session.commit()

            print("Added admin")

            userRole = UserRole(
                userId=admin.id,
                roleId=adminRole.id
            )

            database.session.add(userRole)
            database.session.commit()

            print("Migrations Finished")

            done = True
    except Exception as error:
        print(error)
