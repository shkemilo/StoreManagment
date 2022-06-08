from curses.ascii import isdigit
from datetime import datetime

from Commons.exceptions import BadRequestException
from Store.Commons.models import Category, Order, Product, ProductOrder, database


class CustomerController ():

    def search(productName, categoryName):
        if (productName == None):
            productName = ""
        productSearchPattern = "%{}%".format(productName)
        products = Product.query.filter(
            Product.name.like(productSearchPattern)).all()

        if (categoryName == None):
            categoryName = ""
        categorySearchPattern = "%{}%".format(categoryName)
        categories = Category.query.filter(
            Category.name.like(categorySearchPattern)).all()

        return {"categories": [category.name for category in categories], "products": [product.to_dict() for product in products]}

    def order(customerEmail, requests):
        if(requests == None or len(requests) == 0):
            raise BadRequestException("Field requests is missing.")

        CustomerController.validateOrderRequests()

        order = Order(
            customerEmail=customerEmail,
            timestamp=datetime.datetime.now().isoformat(),
            status="COMPLETE"
        )
        database.session.add(order)
        database.session.commit(order)

        for request in requests:
            productId = request['id']

            productQuantity = request['quantity']

            product = Product.query.filter(Product.id == productId).first()

            received = 0
            if(productQuantity < product.quantity):
                product.quantity -= productQuantity
                received = productQuantity
            else:
                received = product.quantity
                product.quantity = 0

            productOrder = ProductOrder(
                productId=productId,
                orderId=order.id,
                price=product.price,
                received=received,
                requested=productQuantity
            )
            database.session.add(productOrder)
            database.session.commit()

        return order.id

    def status(customerEmail):
        return [order.to_dict() for order in Order.query.filter(Order.customerEmail == customerEmail).all()]

    def validateOrderRequests(requests):
        if(requests == None or len(requests) == 0):
            raise BadRequestException("Field requests is missing.")

        requestCount = 0
        for request in requests:
            productId = request['id']
            if(productId == None):
                raise BadRequestException(
                    "Product id is missing for request number {}.".format(requestCount))

            productQuantity = request['quantity']
            if(productQuantity == None):
                raise BadRequestException(
                    "Product quantity is missing for request number {}.".format(requestCount))

            if(not isdigit(productId)):
                raise BadRequestException(
                    "Invalid product id for request number {}.".format(requestCount))

            if(not isdigit(productQuantity)):
                raise BadRequestException(
                    "Invalid product quantity for request number {}.".format(requestCount))

            product = Product.query.filter(Product.id == productId).first()
            if(product == None):
                raise BadRequestException(
                    "Invalid product for request number {}.".format(requestCount))

            requestCount += 1
