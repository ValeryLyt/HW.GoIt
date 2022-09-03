from datetime import datetime, timedelta


def get_weekday_by_index(weekday_index):
    weekday = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    for day_id, day in weekday.items():
        if day_id == weekday_index:
            day_of_week = day
            return day_of_week


def construct_current_date(date_of_birth: datetime):
    current_year = datetime.now().year
    current_date = datetime(year=current_year, month=date_of_birth.month,
                            day=date_of_birth.day)
    return current_date


def one_week_birthday():
    current_week = datetime.today() + timedelta(days=7)
    return current_week
