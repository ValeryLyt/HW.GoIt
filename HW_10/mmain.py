from collections import UserDict
from typing import Union, Any


class Field:
    def __init__(self, value: str):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class AddressBook(UserDict):

    def add_contact(self, name: Name, phone: Phone = None):
        contact = Record(name=name, phones=phone)
        self.data[name.value] = contact

    def add_record(self, record: "Record"):
        self.data[record.name.value] = record


class Record:
    def __init__(self, name: Name, phones: Phone = None):
        self.name: Name = name
        self.phones: list[Phone] = [phones] if phones is not None else []

    def __repr__(self):
        return f"{self.name.value}: {' '.join(phone.value for phone in self.phones)}"

    def add_contact(self, phone_number: Phone):
        self.phones.append(phone_number)

    def change_contact(self, old_number: Phone, new_number: Phone):
        try:
            self.phones.remove(old_number)
            self.phones.append(new_number)
        except ValueError:
            return f"{old_number} does not exists!"

    def delete_phone(self, phone: Phone):
        try:
            self.phones.remove(phone)
        except ValueError:
            return f"{phone} does not exists!"


def main():
    pass


if __name__ == '__main__':
    main()