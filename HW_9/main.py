import re

phone_book = {}

EXIT_COMMANDS = ('good bye', 'close', 'exit')


def add_new_contact_func(name: str, phone_number: str):

    if name in phone_book:
        result = f'Contact {name} already exists\n'
        return result

    elif not name == False and not phone_number == False:
        phone_book[name] = phone_number
        result = f'New contact {name} with phone number {phone_number} ' \
                 f'has been saved successfully\n'
        return result

    else:
        raise ValueError


def change_phone_numb_func(name: str, phone_number: str):

    if name in phone_book and phone_number != False:
        phone_book[name] = phone_number
        return f'For contact {name} was set new phone number {phone_number}\n'
    elif name == False or phone_number == False:
        raise ValueError
    else:
        return f'There is no such contact {name} ' \
               f'in phone book. Add contact as new one\n'


def input_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
            return result
        except KeyError as ex:
            ex_info = f'Enter correct command, please.'
        except ValueError as ex:
            ex_info = f'Give me correct name or/and phone number.'
        except IndexError as ex:
            ex_info = f'Enter correct data, please.'
        return ex_info
    return wrapper


def show_user_phone_func(name: str):

    if name in phone_book:
        contact_phone_numb = phone_book[name]
        return f'Contact {name} has following phone number {contact_phone_numb}'
    elif name not in phone_book and name != False:
        return f'There is no contact {name} in phone book'
    elif name == False:
        raise ValueError


def parsing_user_input(string: str):
    raw_user_input = re.search(r'(?:^add\b|^change\b|^phone\b)', string)
    command = raw_user_input.group() if raw_user_input else False

    phone_number = ''.join(re.findall('\d+', string))
    if len(phone_number) == 12:
        phone_number = f'+{phone_number}'
    elif len(phone_number) == 10:
        phone_number = f'+38{phone_number}'
    else:
        phone_number = False

    clear_name = re.search(
        r'[^(?:^add\b|^change\b|^phone\b)][a-zA-Z]+', string)
    name = clear_name.group().strip().title() if clear_name else False
    return command, phone_number, name


def handler_func(command, name, phone_number):
    if command == 'add' or command == 'change':
        result = COMMANDS[command](name, phone_number)
    else:
        result = COMMANDS[command](name)
    return result


def main():
    print("COMMANDS:\n<hello>, <add name phone number>, "
          "<change name phone number>, <phone name>\n"
          "To exit enter one of the following commands:\n"
          "<good bye>, <close>, <exit>\n"
          "To show phon book enter <show all>\n")

    while True:

        user_command = input('Waiting for your command:\n')
        user_command = user_command.casefold()

        if user_command in EXIT_COMMANDS:
            print('Good bye!\n')
            break

        elif user_command == 'show all':
            for k, v in phone_book.items():
                print(f'Contact {k} has following phone number {v}')

        elif user_command == 'hello':
            print('How could I help you?\n')

        else:
            command, phone_number, name = parsing_user_input(user_command)
            print(handler_func(command, name, phone_number))


COMMANDS = {
    'add': add_new_contact_func,
    'change': change_phone_numb_func,
    'phone': show_user_phone_func
}

if __name__ == '__main__':
    main()