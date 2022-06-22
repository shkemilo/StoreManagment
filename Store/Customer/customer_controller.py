from datetime import datetime

from sqlalchemy import and_

from Commons.exceptions import BadRequestException
from Store.Commons.models import Category, Order, Product, ProductCategory, ProductOrder, database


class CustomerController ():

    def search(productName, categoryName):
        if (productName == None):
            productName = ""
        productSearchPattern = "%{}%".format(productName)

        if (categoryName == None):
            categoryName = ""
        categorySearchPattern = "%{}%".format(categoryName)

        # Probably could have been done with just one querry
        products = Product.query.join(ProductCategory).join(Category).filter(and_(
            Category.name.like(categorySearchPattern), Product.name.like(productSearchPattern))).all()
        categories = Category.query.join(ProductCategory).join(Product).filter(and_(
            Category.name.like(categorySearchPattern), Product.name.like(productSearchPattern))).all()

        return {"categories": [category.name for category in categories], "products": [product.to_dict() for product in products]}

    def order(customerEmail, requests):
        if(requests == None or len(requests) == 0):
            raise BadRequestException("Field requests is missing.")

        CustomerController.validateOrderRequests(requests)

        order = Order(
            customerEmail=customerEmail,
            timestamp=datetime.now().isoformat()
        )
        database.session.add(order)
        database.session.commit()

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
            if(not 'id' in request):
                raise BadRequestException(
                    "Product id is missing for request number {}.".format(requestCount))
            productId = request['id']

            if(not 'quantity' in request):
                raise BadRequestException(
                    "Product quantity is missing for request number {}.".format(requestCount))
            productQuantity = request['quantity']

            if(not isinstance(productId, int) or productId < 0):
                raise BadRequestException(
                    "Invalid product id for request number {}.".format(requestCount))

            if(not isinstance(productQuantity, int) or productQuantity < 0):
                raise BadRequestException(
                    "Invalid product quantity for request number {}.".format(requestCount))

            product = Product.query.filter(Product.id == productId).first()
            if(product == None):
                raise BadRequestException(
                    "Invalid product for request number {}.".format(requestCount))

            requestCount += 1
