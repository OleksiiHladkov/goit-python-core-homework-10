import re
from rich import print
from rich.table import Table
from collections import UserDict


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
    def __init__(self, name:Name, phones:list[Phone]=list()) -> None:
        self.name = name
        self.phones = phones

    def __str__(self) -> str:
        return f"{self.name} {self.show_phones_list()}"
    
    def new_phones_list(self, phone:Phone) -> None:
        new_phones_list = list()
        new_phones_list.append(phone)
        self.phones = new_phones_list
    
    def add_to_phones_list(self, phone:Phone):
        self.phones.append(phone)
    
    def show_phones_list(self) -> list:
        result = ""
        count = 1
        
        for item in self.phones:
            sep = ", " if count < len(self.phones) else ""
            result += str(item) + sep
            count += 1

        return result


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
    
    def is_name_in_adressbook(self, name:Name) -> bool:
        return name.value in self.data.keys()
    
    def show_phones(self, name:Name) -> Phone:
        record:Record = self.get(name.value)

        if record:
            return f"Successfully finded number '{record.show_phones_list()}' by contact '{name}'"
        else:
            return f"Can't find number by contact '{name}'"
        
    def show_all(self) -> Table:
        result = Table(title="Contacts list")
        result.add_column("Name", justify="center",)
        result.add_column("Phone", justify="center")
        
        for name, record in self.data.items():
            result.add_row(str(name), record.show_phones_list())
        
        return result


def parcing_data(value:str) -> dict:
    """
    Allows to parcing string value, which chunks separated by space.
    Allows to use 'name', which consists of two or more words.
    Available value format: '[command] [name] [phone]' or '[command] [first_name last_name] [phone]'.
    """
    
    result = {"command": ""}

    find_command = False
    count = 1
    start = 0
    
    for lit in value:
        
        is_finish = (count == len(value))
        first_coundition = (lit == " " or is_finish)
        second_coundition = (lit.isnumeric() or lit == "+")
        
        chunk = value[start:count].strip()
        
        if first_coundition and not find_command:
            
            if chunk in tuple(COMMANDS.keys()):
                find_command = True
                result["command"] = chunk
                start = count
        elif (second_coundition or is_finish) and find_command:
            if is_finish:
                if chunk:
                    result["name"] = chunk
            else:
                if chunk[:-1].strip():
                    result["name"] = chunk[:-1].strip()
                if value[count-1:len(value)]:
                    result["phone"] = value[count-1:len(value)]
            break

        count += 1

    return result


def chek_phone(phone:str) -> bool:
    result = re.findall(
        r"(\+\d{1,3}\d{2}\d{6,8})", phone)
    
    return result == list()


def input_error(handler_func):
    def inner_func(**kwargs):
        try:
            if kwargs.get("phone") and chek_phone(kwargs["phone"]):
                raise ValueError()     
            
            result = handler_func(**kwargs)
        except KeyError as key:
            result = f"Name {key} is not found" if not str(key) in ("'name'", "'phone'") else f"You must enter {key}"
        except ValueError:
            result = "Phone number must be in format '+\[country]\[town]\[number]'. Examples: '+380661234567' or '+442012345678'"
        
        return result
    return inner_func


def command_hello(**kwargs) -> str:
    return "How can I help you?"


@input_error
def command_add(**kwargs) -> str:
    name = Name(kwargs["name"])
    phone = Phone(kwargs["phone"])
    
    if adressbook.is_name_in_adressbook(name):
        record:Record = adressbook.get(name.value)
        
        if record:
            record.add_to_phones_list(phone)
            return f"Succesfully added phone '{phone}' to name '{record.name}'"
        else:
            return f"Can't find name '{name}'"
    else:
        record = Record(name)
        record.new_phones_list(phone)
        return adressbook.add_record(record)


@input_error
def command_change(**kwargs) -> str:
    name = Name(kwargs["name"])
    phone = Phone(kwargs["phone"])
    
    record:Record = adressbook.get(name.value)
    
    if record:
        record.new_phones_list(phone)
        return f"Succesfully changed record '{record}'"
    else:
        return f"Can't find name '{name}'"


@input_error
def command_delete(**kwargs) -> str:
    name = Name(kwargs["name"])
    return adressbook.delete_record(name)


@input_error
def command_phone(**kwargs) -> str:
    name = Name(kwargs["name"])
    return adressbook.show_phones(name)


def command_show_all(**kwargs) -> Table:
    return adressbook.show_all()


def command_exit(**kwargs) -> str:
    return "Good bye!"


COMMANDS = {"hello": command_hello,
            "add": command_add,
            "change": command_change,
            "delete": command_delete,
            "phone": command_phone,
            "show all": command_show_all,
            "good bye": command_exit,
            "close": command_exit,
            "exit": command_exit,}


def get_handler(command:str):
    return COMMANDS[command.lower()]


def main():
    while True:
        user_input = input("Enter command: ")
        
        command_dict = parcing_data(user_input)

        command = command_dict.get("command", "")
        
        if command:
            handler = get_handler(command)        
            result = handler(**command_dict)
            
            if command in ("exit", "good bye", "close"):
                print(result, "\n")
                break

            print(result, "\n")
        else:
            print("Can not recognize a command! Please, try again.", "\n")     




if __name__ == "__main__":
    adressbook = AdressBook()
    main()
    