from collections import defaultdict
from datetime import datetime
from typing import Dict
from chek_current_birthday import construct_current_date, one_week_birthday, get_weekday_by_index

USERS = [{"Lera": datetime(year=1997, month=8, day=5)},
         {"Vasya": datetime(year=1994, month=12, day=7)},
         {"Lubov": datetime(year=1990, month=9, day=4)},
         {"Petya": datetime(year=2000, month=9, day=7)},
         {"Stas": datetime(year=1995, month=9, day=5)},
         {"Dasha": datetime(year=1994, month=9, day=8)}
         ]


def get_birthdays_per_week(users: list):
    greeting_scheduler: Dict[str: list] = defaultdict(list)

    for user_dict in users:
        for user_name, birthday in user_dict.items():
            current_birthday = construct_current_date(birthday)
            current_week = one_week_birthday()
            current_day = datetime.today()
            if current_day < current_birthday < current_week:
                index_day_of_birthday = current_birthday.weekday()
                weekday = get_weekday_by_index(index_day_of_birthday)
                if weekday in ["Saturday", "Sunday"]:
                    weekday = "Monday"
                greeting_scheduler[weekday].append(user_name)
    for weekday, birthday_name in greeting_scheduler.items():
        print(f"{weekday}: " + ", ".join(birthday_name))


if __name__ == '__main__':
    get_birthdays_per_week(USERS)
