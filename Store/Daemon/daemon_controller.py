import json
import flask
from redis import Redis
from Store.Commons.models import Cateogry, Product, ProductCategory, database

from Store.Daemon.configuration import Configuration


class DaemonController():
    
    logger = flask.current_app.logger

    def consumeProducts():
        DaemonController.logger.info('Consume products daemon thread started.')
        while(True):
            DaemonController.logger.info('Wating for product.')
            productJson = None
            with Redis(host=Configuration.REDIS_HOST) as redis:
                productJson = redis.blpop(Configuration.REDIS_HOST)
            
            productData = json.load(productJson)
            name = productData['name']
            quantity = productData['quantity']
            price = productData['price']
            categories = productData['categories']

            product = Product.query.filter(Product.name == name).first()
            if(not product):
                product = Product(name=name, quantity=quantity, price=price)
                database.session.add(product)
                database.session.commit()

                for categoryName in categories:
                    category = Cateogry.query.filter(
                        Cateogry.name == categoryName).first()

                    if (not category):
                        category = Cateogry(name=categoryName)
                        database.session.add(category)
                        database.session.commit()

                    productCategory = ProductCategory(
                        productId=product.id, categoryId=category.id)
                    database.session.add(productCategory)
                    database.session.commit()
            else:
                if(set(product.categories) != set(categories)):
                    continue

                product.price = DaemonController.calculateNewPrice(product.quantity, product.price, quantity, price)
                product.quantity += quantity
                database.session.commit()

    def calculateNewPrice(currentQuantity, currentPrice, deliveredQuantity, deliveredPrice):
        return (currentQuantity * currentPrice + deliveredQuantity * deliveredPrice) / (currentQuantity + deliveredQuantity)
