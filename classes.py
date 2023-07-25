from collections import UserDict
from rich.table import Table


PAGINATION = 4


class Field:
    def __init__(self, value: str) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return self.value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name:Name, phone:Phone=None) -> None:
        self.name = name
        self.phones = []

        if phone:
            self.phones.append(phone)

    def add_phone(self, phone:Phone):
        if str(phone) not in [str(p) for p in self.phones]:
            self.phones.append(phone)
            return f"Succesfully added phone '{phone}' to name '{self.name}'"
        else:
            return f"Phone '{phone}' is already in record '{self}'"

    def __str__(self) -> str:
        return f"{self.name} {', '.join(str(p) for p in self.phones)}"
    

class AdressBook(UserDict):
    def add_record(self, record:Record) -> str:
        self.data[record.name.value] = record
        return f"Succesfully added record '{record}'"
        
    def delete_record(self, name) -> str:
        current_record = self.data.pop(name.value)
        
        if current_record:
            return f"Succesfully deleted record '{current_record}'"
        else:
            return f"Can't find name '{name}'"
    
    def show_phones(self, name:Name) -> Phone:
        record:Record = self.get(name.value)

        if record:
            return f"Successfully finded number '{record.show_phones_list()}' by contact '{name}'"
        else:
            return f"Can't find number by contact '{name}'"
            
    def show_all(self) -> list[Table]:
        result = Table(title="Contacts list")
        result.add_column("Name", justify="center",)
        result.add_column("Phone", justify="center")

        for name, record in self.data.items():
            result.add_row(str(name), '\n'.join(str(p) for p in record.phones))

        return result