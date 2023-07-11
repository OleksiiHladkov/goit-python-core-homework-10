import re
from rich import print
from rich.table import Table


contacts = {}


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
            result = f"You must enter {key}"
        except ValueError:
            result = result = "Phone number must be in format '+\[country]\[town]\[number]'. Examples: '+380661234567' or '+442012345678'"
        
        return result
    return inner_func


def command_hello(**kwargs) -> str:
    return "How can I help you?"


@input_error
def command_add(**kwargs) -> str:
    name = kwargs["name"]
    phone = kwargs["phone"]
    contacts[name] = phone
    
    return f"Successfully added contact '{name}' with number '{phone}'"


@input_error
def command_change(**kwargs) -> str:
    name = kwargs["name"]
    phone = kwargs["phone"]
    contacts[name] = phone
    
    return f"Successfully changed contact '{name}' with number '{phone}'"
    

@input_error
def command_phone(**kwargs) -> str:
    name = kwargs["name"]
    phone = contacts.get(name)
    
    return f"Successfully finded number '{phone}' by contact '{name}'"


def command_show_all(**kwargs) -> Table:
    result = Table(title="Contacts list")
    result.add_column("Name", justify="center",)
    result.add_column("Phone", justify="center")
    
    for name, phone in contacts.items():
        result.add_row(name, phone)
    
    return result


def command_exit(**kwargs) -> str:
    return "Good bye!"


COMMANDS = {"hello": command_hello,
            "add": command_add,
            "change": command_change,
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
    main()
    