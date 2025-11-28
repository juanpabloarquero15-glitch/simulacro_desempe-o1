import csv
import os
import re
from usuarios import User; from equipos import Equipment;
class Borrow:
    __max_id = 0
    __borrow_record = {}
    equipment : Equipment
    user : User

    #prestamo_id, equipo_id, nombre_equipo, usuario_prestatario, tipo_usuario, fechas, días, retraso, estado, mes, anio
    def __init__(self, id, equipment_id, equipment_name, borrowing_username, user_type, state, petition_date, aproved_date, returned_date):
        self.id = id
        self.equipment_id = equipment_id
        self.equipment_name = equipment_name
        self.user_type = user_type
        self.petition_date = petition_date
        self.aproved_date = aproved_date
        self.state = state
        self.month = returned_date

    @classmethod
    def create(cls, equipment_id, equipment_name, borrowing_username, user_type, state, petition_date, aproved_date = None, returned_date = None, id = None):
        date_pattern = re.compile(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$")
        if id == None:
            id = cls.__max_id
        if state not in ["pending", "going", "done"]:
            print("The state for a borrow given is not valid, only \"pending\", \"going\" and \"")
            return None
        elif user_type not in ["student", "Instructor", "administrator"]:
            print(f"The user type given ({user_type}) is not valid")
            return None
        elif petition_date != None or not re.match(date_pattern, petition_date):
            print("The petition date format is inválid: format must be dd/mm/yyyy (all integer numbers)")
            return None
        elif aproved_date != None or not re.match(date_pattern, aproved_date):
            print("The aproved date format is inválid: format must be dd/mm/yyyy (all integer numbers)")
            return None
        elif returned_date != None or not re.match(date_pattern, returned_date):
            print("The returned date format is inválid: format must be dd/mm/yyyy (all integer numbers)")
            return None        
        cls.__max_id = id+1

        new_borrow = cls(id, equipment_name, borrowing_username, user_type, state, petition_date, aproved_date, returned_date, id)
        if returned_date != None:
            return new_borrow   #Do not create attributes equipment and user on borrow
        
        equipment = Equipment.get_equipment_w_id(equipment_id)
        user = User.get_user_w_username(borrowing_username)
        
        if equipment == None or user == None:
            print("the equipment id does not exists")
            return None #Since the equipment and user_id don't exist, it means the values given are false for the program, ergo, return none
        
        new_borrow.equipment = equipment
        new_borrow.user = user
        return new_borrow

    @classmethod
    def calculateBorrowTime(cls, user:User, equipment:Equipment):
        pass