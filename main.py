import re
from classes import Name, Phone, Record, AdressBook, Table
from rich import print



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
    
    record:Record = adressbook.get(name.value)
    
    if record:
        return record.add_phone(phone)
    else:
        record = Record(name, phone)
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

            if isinstance(result, (list, tuple)):
                # printing list of Tables or tuple of Tables (pagination)
                print(*result, "\n")
            else:
                print(result, "\n")
        else:
            print("Can not recognize a command! Please, try again.", "\n")     




if __name__ == "__main__":
    adressbook = AdressBook()
    main()
    