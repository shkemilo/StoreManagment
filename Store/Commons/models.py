from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

database = SQLAlchemy()


class ProductCategory (database.Model):
    __tablename__ = "productcategory"

    id = database.Column(database.Integer, primary_key=True)

    productId = database.Column(
        database.Integer, database.ForeignKey("product.id"), nullable=False)
    categoryId = database.Column(
        database.Integer, database.ForeignKey("category.id"), nullable=False)


class ProductOrder (database.Model):
    __tablename__ = "productorder"

    id = database.Column(database.Integer, primary_key=True)

    productId = database.Column(
        database.Integer, database.ForeignKey("product.id"), nullable=False)
    orderId = database.Column(
        database.Integer, database.ForeignKey("order.id"), nullable=False)

    price = database.Column(database.Float, nullable=False)
    received = database.Column(database.Integer, nullable=False)
    requested = database.Column(database.Integer, nullable=False)

    def is_completed(self):
        return self.received == self.requested

    def to_dict(self):
        product = Product.query.filter(
            ProductOrder.productId == self.productId).first()
        return {
            "categories": product.categories,
            "id": self.productId,
            "name": product.name,
            "price": self.price,
            "received": self.received,
            "requested": self.request
        }


class Product (database.Model):
    __tablename__ = "product"

    id = database.Column(database.Integer, primary_key=True)

    name = database.Column(database.String(256), nullable=False, unique=True)
    quantity = database.Column(database.Integer, nullable=False)
    price = database.Column(database.Float, nullable=False)

    categories = database.relationship(
        "Category", secondary=ProductCategory.__table__, back_populates="products")

    orders = database.relationship(
        "Product", secondary=ProductOrder.__table__, back_populates="products")

    def to_dict(self):
        return {
            "categories": [category.name for category in self.categories],
            "id": self.id, "name": self.name,
            "price": self.price, "quantity": self.quantity}

    def get_product_orders(self):
        return ProductOrder.query.filter(ProductOrder.productId == self.id).all()

    def get_pending_product_orders(self):
        return ProductOrder.query.filter(and_(ProductOrder.productId == self.id, ProductOrder.received == ProductOrder.requested)).all()


class Category (database.Model):
    __tablename__ = "category"

    id = database.Column(database.Integer, primary_key=True)

    name = database.Column(database.String(256), nullable=False, unique=True)

    products = database.relationship(
        "Product", secondary=ProductCategory.__table__, back_populates="categories")


class Order (database.Model):
    __tablename__ = "order"

    id = database.Column(database.Integer, primary_key=True)

    customerEmail = database.Column(database.String(256), nullable=False)

    timestamp = database.Column(database.DateTime, nullable=False)

    products = database.relationship(
        "Product", secondary=ProductOrder.__table__, back_populates="orders")

    def get_product_orders(self):
        return ProductOrder.query.filter(ProductOrder.orderId == self.id).all()

    def get_pending_product_orders(self):
        return ProductOrder.query.filter(and_(ProductOrder.orderId == self.id, ProductOrder.received == ProductOrder.requested)).all()

    def get_status(self):
        return "COMPLETED" if (len(self.get_pending_product_orders()) == 0) else "PENDING"

    def get_price(self):
        price = 0
        for productOrder in self.get_product_orders():
            price += productOrder.price
        return price

    def to_dict(self):
        return {
            "products": [productOrder.to_dict() for productOrder in self.get_product_orders()],
            "price": self.get_price(),
            "status": self.get_status(),
            "timestamp": self.timestamp
        }
