from email.utils import parseaddr
import re

from commons.models import database, User, UserRole


class AuthenticationController ():
    def register(self, forename: str, surname: str, email: str, password: str, isCustomer: bool):
        result = {}
        if(forename == None or len(forename) == 0):
            result["message"] = "Field forename is missing."
            return [False, result]
        if(surname == None or len(surname) == 0):
            result["message"] = "Field surname is missing."
            return [False, result]
        if(email == None or len(email) == 0):
            result["message"] = "Field email is missing."
            return [False, result]
        if(password == None or len(password) == 0):
            result["message"] = "Field password is missing."
            return [False, result]
        if(isCustomer == None):
            result["message"] = "Field isCustomer is missing."
            return [False, result]

        parsedEmail = parseaddr(email)
        if (len(parsedEmail[1] == 0)):
            result["message"] = "Invalid email."
            return [False, result]

        passwordOk = re.fullmatch(
            r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$',
            password)
        if(not passwordOk):
            result["message"] = "Invalid password."
            return [False, result]

        emailFound = database.session.query(
            User).filter_by(email=email).first() != None
        if(emailFound):
            result["message"] = "Email already exists."
            return [False, result]

        user = User(email=email, password=password,
                    forename=forename, surname=surname)
        database.session.add(user)
        database.session.commit()

        roleId = 2 if isCustomer else 3

        userRole = UserRole(userId=user.id, roleId=roleId)
        database.session.add(userRole)
        database.session.commit()

        result["message"] = "Registration successful!"
        return [True, result]
