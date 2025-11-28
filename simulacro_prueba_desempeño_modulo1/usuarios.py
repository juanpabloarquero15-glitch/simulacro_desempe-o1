import os
import csv
from equipos import Equipment
class User:
    __are_admins = False
    __criptid = ["_","a","6","d","m","7","h","ñ","8","e","i","l","2","j","c","f","v","4","g","b","9","n","y","k","$","5","q","t","r","x","o","1","s","p","u","0","z","3"]
    __users = {} #Dictionay to easy user validation
    __users_path = os.path.normpath("csv_archives"+os.path.pathsep+"users.csv")
    equipment_in_posesion : list[Equipment] #Shoul be a list of Equipments
    
    def __init__(self, username, password, rol, email): #The constructor MUST NOT be called directly to create users
        """
        Constructor
        """
        self.username = username
        self.password = password #Encrypts password
        self.email = email
        self.rol = rol
    
    @classmethod
    def create(cls, username, password, rol, email = None):
        """
        Class method for creation of users
        Use instead of normal constructor
        Makes verifications, allow user creation if passes all verifications
        Else returns None
        """
        if username in cls.__users or username == "": #usernames must be unique (As there no ID)
            print("UserName not avaible, try another")
            return None
        elif password=="":
            print("The password cannot be empty")
            return None
        elif rol=="admin" and cls.__are_admins == False:
            cls.__are_admins = True  #Makes sure to change the User class attribute and not the instance
            return cls(username, cls.encryptPassword(password), rol, email)
        elif rol == "admin" and cls.__are_admins == True:
            print("There is already an admin user, cannot create more")
            return None
        elif rol not in ["student", "Instructor", "administrator"]:
            print("Invalid rol, only student, instructor or admin are valid")
            return None
        else:
            new_user = cls(username, cls.encryptPassword(password), rol, email) #returns the construction of the object
            cls.__users[new_user.username] = new_user

    @classmethod
    def encryptPassword(cls, password):
        """
        Encrypts the password with a handmade method
        returns the encrypted password
        """
        encrypted = ""
        new_indexation = lambda x: (x*2)-38
        for ch in password:
            if ch in cls.__criptid:
                i = cls.__criptid.index(ch)
                encrypted += cls.__criptid[new_indexation(i)]
            else:
                encrypted += "*/-"
        return encrypted
    @classmethod
    def sign_in(cls, username, password, tr = 1):
        """
        Classmethod to sign in as an already existing user
        Receives username and password
        Verifies if username exist on memory
        returns tuple user, true if login succesfull
        if login unsuccesfull makes a callback to itself, up to 3 times
        if the 3 times are up, returns tuple None, False
        if the user does not exists, returns tuple None, True
        """
        encripted = cls.encryptPassword(password)
        if tr == 4:
            return None, False
        if username in cls.__users:
            if cls.__users[username].password == encripted:
                print("Login succesfull")
                return cls.__users[username], True
            else:
                return cls.sign_in(username, password, tr+1)
        else:
            print("No such user in the database")
            return None, True

    @classmethod
    def charge_users(cls):
        """
        Classmethod to charge the users stored on the csv file
        Returns True if succesfully charged, else False
        """
        if not os.path.exists(cls.__users_path):
            print("The users.csv archive does not exist or is in another path")
            return False
        with open(cls.__users_path, "r", newline="") as archive:
            reader = csv.reader(archive)
            next(reader)
            for user in reader:
                cls.create(user[0], user[1], user[2], user[3])
        return True
    
    @classmethod
    def save_user(cls, user):
        """
        Saves the user on the csv archive
        ONLY call for first time insertion
        returns True if saved, else False
        """
        dir  = os.path.dirname(cls.__users_path)
        if not os.path.exists(dir):
            if not cls.create_directory():
                print("The users.csv archive wasn't created")
                return False
        with open(cls.__users_path, "a", newline="") as users:
            writer = csv.writer(users)
            writer.writerow(user.get_user())
        return True
    
    @classmethod
    def create_directory(cls):
        """
        Creates the directory for the csv storing
        Creates the csv archive on the path and creates the header row
        """
        try:
            dir = os.path.dirname(cls.__users_path)
            os.mkdir(dir)
            with open(cls.__users_path, "w") as users:
                writer = csv.writer(users)
                writer.writerow(["user", "password", "rol", "email"])
        except Exception as ex:
            print(f"Error, exception: {ex} creating the {dir} directory to save users")
            return False
        return True
    
    @classmethod
    def get_user_w_username(cls, username):
        if username in cls.__users:
            return cls.__users[username]
        print("No user with that username")
        return None
    
    def isAdmin(self):
        """
        Simple method to verify admin status
        """
        if self.rol == "admin":
            return True
        return False
    
    def get_user(self):
        """
        user getter
        returns list with all user parameters
        """
        return [self.username, self.password, self.rol, self.email]
    
    def get_rol(self):
        """
        rol getter
        returns user's rol
        """
        return self.rol
    
    def get_email(self):
        """
        email getter
        returns user's email
        """
        if self.email=="":
            return None
        return self.email
    
    def return_equipment(self, equipment_id, status)->bool:
        """
        receives status parameter from the user (Damaged or invalid)
        Receives equipment id to return
        Return True if equipment is returned, else False
        """
        valid_status = ["available", "damaged"]
        if status not in valid_status:
            print(f"Error, {status} is not a valid status to return a equipment, only available or damaged")
            return False
        if len(self.equipment_in_posesion)==0:
            return False
        for equipment in self.equipment_in_posesion:
            if equipment.id == equipment_id:
                equipment.return_equipment()
                return True
        return False
    