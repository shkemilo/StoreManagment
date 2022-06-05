from Authentication.models import database


def init_db(application):
    with application.app_context() as context:
        from Authentication.models import User, Role, UserRole

        application.logger.info("Database initalization starting")

        application.logger.info("Creating schema")

        database.create_all()
        database.session.commit()

        application.logger.info("Creating roles")

        adminRole = Role(name="admin")
        customerRole = Role(name="customer")
        workerRole = Role(name="worker")

        database.session.add(adminRole)
        database.session.add(customerRole)
        database.session.add(workerRole)
        database.session.commit()

        application.logger.info("Creating admin user")

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

        database.session.add(userRole)
        database.session.commit()

        application.logger.info("Database initalization finished")
