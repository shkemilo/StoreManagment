from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class ProductCategory (database.Model):
    __tablename__ = "productcategory"

    id = database.Column(database.Integer, primary_key=True)

    productId = database.Column(
        database.Integer, database.ForeignKey("product.id"), nullable=False)
    categoryId = database.Column(
        database.Integer, database.ForeignKey("category.id"), nullable=False)


class Product (database.Model):
    __tablename__ = "product"

    id = database.Column(database.Integer, primary_key=True)

    name = database.Column(database.String(256), nullable=False, unique=True)
    quantity = database.Column(database.Integer, nullable=False)
    price = database.Column(database.Float, nullable=False)

    categories = database.relationship(
        "Category", secondary=ProductCategory.__table__, back_populates="products")


class Cateogry (database.Model):
    __tablename__ = "category"

    id = database.Column(database.Integer, primary_key=True)

    name = database.Column(database.String(256), nullable=False)

    products = database.relationship(
        "Product", secondary=ProductCategory.__table__, back_populates="categories")
