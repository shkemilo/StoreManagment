import json
from redis import Redis
from Store.Commons.models import Category, Order, Product, ProductCategory, ProductOrder, database

from Store.Daemon.configuration import Configuration


class DaemonController():

    def consumeProducts(application):
        with application.app_context() as context:
            application.logger.info(
                'Consume products daemon thread started.')
            while(True):
                application.logger.info('Wating for product.')
                productJson = None
                with Redis(host=Configuration.REDIS_HOST) as redis:
                    productJson = redis.blpop(
                        Configuration.REDIS_PRODUCTS_LIST)[1]
                application.logger.info('Product consumed.')

                productData = json.loads(productJson)
                name = productData['name']
                quantity = productData['quantity']
                price = productData['price']
                categories = productData['categories']

                product = Product.query.filter(Product.name == name).first()
                if(not product):
                    application.logger.info(
                        'Product not in DB. Create new product.')

                    product = Product(
                        name=name, quantity=quantity, price=price)
                    database.session.add(product)
                    database.session.commit()

                    for categoryName in categories:
                        category = Category.query.filter(
                            Category.name == categoryName).first()

                        if (not category):
                            category = Category(name=categoryName)
                            database.session.add(category)
                            database.session.commit()

                        productCategory = ProductCategory(
                            productId=product.id, categoryId=category.id)
                        database.session.add(productCategory)
                        database.session.commit()
                else:
                    application.logger.info('Product in DB. Update product.')

                    categoryNames = set(
                        [category.name for category in product.categories])
                    if(categoryNames != set(categories)):
                        application.logger.warning(
                            'Different product categories in input. Discarding product update.')
                        application.logger.warning(categoryNames)
                        application.logger.warning(set(categories))
                        continue

                    # Weird hack to update the quantity value
                    product.quantity = Product.quantity
                    database.session.commit()

                    product.price = DaemonController.calculateNewPrice(
                        product.quantity, product.price, quantity, price)
                    product.quantity = Product.quantity + quantity
                    database.session.commit()

                    pendingProductOrders = product.get_pending_product_orders()

                    for pendingProductOrder in pendingProductOrders:
                        product.quantity = Product.quantity
                        pendingProductOrder.received = ProductOrder.received
                        database.session.commit()

                        itemsLeft = pendingProductOrder.requested - pendingProductOrder.received
                        if(itemsLeft <= product.quantity):
                            product.quantity = Product.quantity - itemsLeft
                            pendingProductOrder.received = pendingProductOrder.requested
                            database.session.commit()
                        else:
                            pendingProductOrder.received = ProductOrder.received + product.quantity
                            product.quantity = 0
                            database.session.commit()
                            break

                    application.logger.info("Updated product: " + product.name)

    def calculateNewPrice(currentQuantity, currentPrice, deliveredQuantity, deliveredPrice):
        return (currentQuantity * currentPrice + deliveredQuantity * deliveredPrice) / (currentQuantity + deliveredQuantity)
