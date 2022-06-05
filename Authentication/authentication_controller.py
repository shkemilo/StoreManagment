from email.utils import parseaddr
import re
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy import and_
from Commons.exceptions import BadRequestException
from Authentication.models import database, User, UserRole


class AuthenticationController ():
    def register(forename: str, surname: str, email: str, password: str, isCustomer: bool):
        if(forename == None or len(forename) == 0):
            raise BadRequestException("Field forename is missing.")
        if(surname == None or len(surname) == 0):
            raise BadRequestException("Field surname is missing.")
        if(email == None or len(email) == 0):
            raise BadRequestException("Field email is missing.")
        if(password == None or len(password) == 0):
            raise BadRequestException("Field password is missing.")
        if(isCustomer == None):
            raise BadRequestException("Field isCustomer is missing.")

        parsedEmail = parseaddr(email)
        if (len(parsedEmail[1]) == 0):
            raise BadRequestException("Invalid email.")

        passwordOk = re.fullmatch(
            r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$',
            password)
        if(not passwordOk):
            raise BadRequestException("Invalid password.")

        emailFound = User.query.filter(User.email == email).first()
        if(emailFound):
            raise BadRequestException("Email already exists.")

        user = User(email=email, password=password,
                    forename=forename, surname=surname)
        database.session.add(user)
        database.session.commit()

        roleId = 2 if isCustomer else 3

        userRole = UserRole(userId=user.id, roleId=roleId)
        database.session.add(userRole)
        database.session.commit()

    def login(email: str, password: str):
        if(email == None or len(email) == 0):
            raise BadRequestException("Field email is missing.")
        if(password == None or len(password) == 0):
            raise BadRequestException("Field password is missing.")

        parsedEmail = parseaddr(email)
        if (len(parsedEmail[1]) == 0):
            raise BadRequestException("Invalid email.")

        user = User.query.filter(
            and_(User.email == email, User.password == password)).first()
        if (not user):
            raise BadRequestException("Invalid credentials.")

        additionalClaims = {
            "forename": user.forename,
            "surname": user.surname,
            "roles": [str(role) for role in user.roles]
        }

        accessToken = create_access_token(
            identity=user.email, additional_claims=additionalClaims)
        refreshToken = create_refresh_token(
            identity=user.email, additional_claims=additionalClaims)

        return {"accessToken": accessToken, "refreshToken": refreshToken}

    def delete(email):
        if(email == None or len(email) == 0):
            raise BadRequestException("Field email is missing.")

        parsedEmail = parseaddr(email)
        if (len(parsedEmail[1]) == 0):
            raise BadRequestException("Invalid email.")

        targetUser = User.query.filter(User.email == email).first()
        if(not targetUser):
            raise BadRequestException("Unknown user.")

        database.session.delete(targetUser)
        database.session.commit()
