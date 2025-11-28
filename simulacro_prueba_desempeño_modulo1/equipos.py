import csv
import os
import re
class Equipment:
    __max_id:int = 0
    __equipment_path = os.path.normpath("csv_archives"+os.path.pathsep+"equipments.csv")
    __equipments = {}

    def __init__(self, id, name, category, actual_state, registration_date):
        self.name = name
        self.category = category
        self.actual_state = actual_state
        self.registration_date= registration_date
        self.id = id 

    @classmethod
    def create(cls, name, category, actual_state = "available", registration_date = None, id = None):
        date_pattern = re.compile(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$")
        if id == None:
            id = cls.__max_id
        if name == "":
            print("El nombre no puede estar vacio")
            return None
        elif category == "":
            print("Debe ingresar una categoria")
            return None
        elif actual_state not in ["available", "borrowed", "damaged", "in-repair"]:
            print("The state is invalid, only available, borrowed, damaged, in-repair")
            return None
        elif registration_date != None and not re.match(date_pattern,registration_date):
            print("The registration date must be None or a string following the pattern: dd/mm/yyyy")
            return None
        else:
            cls.__max_id == id+1
            new_equipment = cls(id, name, category, actual_state, registration_date)
            cls.__equipments[new_equipment.id] = new_equipment
            return new_equipment
    
    @classmethod
    def create_directory(cls):
        """
        Creates the equipments.csv arhive and csv_archives if they don't exist
        returns True if created, else False 
        """
        dir  = os.path.dirname(cls.__equipment_path)
        try: 
            os.mkdir(dir)
            with open(cls.__equipment_path, "w", newline="") as archive:
                writer = csv.writer(archive)
                writer.writerow(["id", "name", "category", "actual_state", "registration_date"])
        except Exception as ex:
            print(f"The directory couldn't be created, exception: {ex}")
            return False
        return True
    
    @classmethod
    def save_equipment(cls, equipment):
        """
        Saves the user on the csv archive
        ONLY call for first time insertion
        returns True if saved, else False
        """
        dir  = os.path.dirname(cls.__equipment_path)
        if not os.path.exists(dir):
            if not cls.create_directory():
                print("The csv archive wasn't created, the equipment cannot be saved")
                return False
        with open(cls.__equipment_path, "a", newline="") as equipments:
            writer = csv.writer(equipments)
            writer.writerow(equipment.get_equipment())
        return True
    
    @classmethod
    def get_equipment_w_id(cls, id):
        if id in cls.__equipments:
            return cls.__equipments[id]
        print(f"No equipment with id {id}")
        return None
    
    def lend_equipment(self)->bool:
        """
        Changes the state of the Equipment object to "borrowed" and returns True
        If the state is diferent than "available", return False
        """
        if self.actual_state == "available":
            self.actual_state = "borrowed"
            return True
        else:
            print(f"The equipment can't be lend, since is {self.actual_state}")
            return False
        
    def return_equipment(self, state)->bool:
        """
        Receives the equipment state
        Returns True if the return is succesfull
        else returns False
        """
        if self.actual_state == "borrowed":
            self.actual_state = state
            if state == "damaged":
                return True
            else:
                self.user_in_posesion = None
                return True
        return False
    
    def get_equipment(self):
        """
        Returns the object attributes inside a list
        the order is [id, name, category, actual_state, registration_date]
        """
        return [self.id, self.name, self.category, self.actual_state, self.registration_date]
    

    def repair_equipment(self, date_return):
        pass