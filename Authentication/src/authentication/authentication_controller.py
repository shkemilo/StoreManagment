from email.utils import parseaddr
import re

from commons.models import database, User, UserRole


class AuthenticationController ():
    def register(self, forename: str, surname: str, email: str, password: str, isCustomer: bool):
        if(forename == None or len(forename) == 0):
            return [False, "Field forename is missing."]
        if(surname == None or len(surname) == 0):
            return [False, "Field surname is missing."]
        if(email == None or len(email) == 0):
            return [False, "Field email is missing."]
        if(password == None or len(password) == 0):
            return [False, "Field password is missing."]
        if(isCustomer == None):
            return [False, "Field isCustomer is missing."]

        parsedEmail = parseaddr(email)
        if (len(parsedEmail[1] == 0)):
            return [False, "Invalid email."]

        passwordOk = re.fullmatch(
            r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$',
            password)
        if(not passwordOk):
            return [False, "Invalid password."]

        emailFound = database.session.query(
            User).filter_by(email=email).first() != None
        if(emailFound):
            return [False, "Email already exists."]

        user = User(email=email, password=password,
                    forename=forename, surname=surname)
        database.session.add(user)
        database.session.commit()

        roleId = 2 if isCustomer else 3

        userRole = UserRole(userId=user.id, roleId=roleId)
        database.session.add(userRole)
        database.session.commit()

        return [True, "Registration successful!"]
