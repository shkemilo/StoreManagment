from Store.Commons.models import database


def init_db(application):
    with application.app_context() as context:
        from Store.Commons.models import Product, Category, ProductCategory

        application.logger.info("Database initalization starting")

        application.logger.info("Creating schema")

        database.create_all()
        database.session.commit()

        application.logger.info("Database initalization finished")
