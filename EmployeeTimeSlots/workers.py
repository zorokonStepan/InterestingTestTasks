import datetime
import numpy as np

from utilites.mail import EmailYandex
from database.db import DataBase


class Employee:
    """The class Employee represents an employee of the company"""

    def __init__(
            self, first_name: str, patronymic: str, last_name: str, date_birth: datetime.date, gender: str, post: str,
            salary: int, start_work: datetime.time, stop_work: datetime.time, email: str = None):

        self.first_name = first_name
        self.patronymic = patronymic
        self.last_name = last_name
        self.date_birth = date_birth
        self.gender = gender
        self.post = post
        self.__salary = salary
        self.email = email
        self.working_hours = WorkingHours(start_work, stop_work)

        db = DataBase()
        db.create_obj(self)
        db.disconnect()

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    def __call__(
            self, user: str, passwd: str, message: str = "Прием! Проверка связи.", subject: str = 'Тестовое письмо.'):
        """send an email to an employee using Yandex
        user - sender's mailing address, for example: example@yandex.ru
        passwd - sender's mailing password"""
        if self.email:
            email_yandex = EmailYandex(user=user, passwd=passwd)
            email_yandex.send_message(adress=self.email, subject=subject, message=message)

    def __del__(self):
        db = DataBase()
        db.delete_obj(self)
        db.disconnect()
        print(f"Работник {str(self)} больше не числиться в нашей компании.")

    @property
    def salary(self):
        db = DataBase()
        db.get_obj(self)
        db.disconnect()
        return self.__salary

    @salary.setter
    def salary(self, value):
        if isinstance(value, int):
            db = DataBase()
            db.update_obj(self)
            db.disconnect()
            self.__salary = value


class WorkingHoursFreeTime:
    """With the help of this class, you can get free slots"""
    def __init__(self, step, pool):
        self.step = step  # minutes
        self.len_row = int(60 / self.step)  # number of cells in 1 hour
        self.pool = pool

    def get_free_time(self):
        """Get free employee slots"""
        free_time_indexes = self.get_free_time_as_index()
        free_time = []
        if free_time_indexes:
            for period in free_time_indexes:
                free_time.append(self.convert_index_to_time(period[0], period[1]))
        return free_time

    def get_free_time_as_index(self):
        """Get the indexes of the beginning and end of free time slots in the form of a list of tuples"""
        flag_start = False
        free_time_indexes = []

        for ind, elem in enumerate(self.pool):
            if elem == 0:
                if not flag_start:
                    start = ind
                    flag_start = True
                else:
                    if ind == (len(self.pool) - 1) or self.pool[ind + 1] != 0:
                        stop = ind
                        free_time_indexes.append((start, stop))
                        flag_start = False
        return free_time_indexes

    @staticmethod
    def convert(ind, len_row, step):
        hour = ind // len_row
        minute = ind % len_row * step
        return hour, minute

    def convert_index_to_time(self, ind_start, ind_stop):
        """Converting free time slots into a readable view"""
        start_hour, start_minute = self.convert(ind=ind_start, len_row=self.len_row, step=self.step)
        stop_hour, stop_minute = self.convert(ind=ind_stop, len_row=self.len_row, step=self.step)

        return f'{datetime.time(start_hour, start_minute).isoformat(timespec="minutes")} - ' \
               f'{datetime.time(stop_hour, stop_minute).isoformat(timespec="minutes")}'


class WorkingHours(WorkingHoursFreeTime):
    """Class of working hours and free slots during working hours for the current day"""

    def __init__(self, start_work: datetime.time, stop_work: datetime.time, step=1, pool=None):
        """
        self.pool - a numpy array in which each cell is a time slot for a day equal to self.step minutes
        np.nan value in non-working time cells
        the value is 0 in meeting-free cells
        the value is 1 in the cells occupied by meetings

        self.meeting - the dictionary in which the meetings are recorded, for checking for deletion.
        if you do it through a database, you need to change it
        """
        WorkingHoursFreeTime.__init__(self, step, pool)
        self.start = start_work
        self.stop = stop_work
        self.pool = self.create_pool()  # nd.array representing all the time in a day
        self.meeting = dict()

    def create_pool(self):
        pool = np.full(self.len_row * 24, np.nan)  # per day, I fill in np.nan all cells
        ind_start_work, ind_stop_work = self.get_indexes(start=self.start, stop=self.stop)
        # I fill in 0 all cells of working time
        pool[ind_start_work:ind_stop_work] = np.nan_to_num(pool[ind_start_work:ind_stop_work], 0)
        return pool

    def get_indexes(self, start: datetime.time, stop: datetime.time):
        """find cell indexes in pool"""
        ind_start = start.hour * self.len_row + int(start.minute / self.step)
        ind_stop = (stop.hour * self.len_row + int(stop.minute / self.step))
        return ind_start, ind_stop

    def get_working_hours(self):
        return f'Working: {self.start.isoformat(timespec="minutes")} - {self.stop.isoformat(timespec="minutes")}'

    def add_meeting(self, start_meet: datetime.time, stop_meet: datetime.time):
        if self.is_valid_time(start_meet, stop_meet):
            ind_start, ind_stop = self.get_indexes(start_meet, stop_meet)
            # if all cells are from 0, then there is a place, we will add a meeting
            if not np.any(self.pool[ind_start:ind_stop]):
                self.pool[ind_start:ind_stop] += 1
                meet = f'{start_meet.isoformat(timespec="minutes")} - {stop_meet.isoformat(timespec="minutes")}'
                self.meeting[meet] = True
                return 'Встреча добавлена'
            else:
                if np.all(self.pool[ind_start:ind_stop]):
                    return "Время полностью занято"
                return "Время частично занято"
        return 'Время не подходит'

    def del_meeting(self, start_meet: datetime.time, stop_meet: datetime.time):
        """remove the meeting"""
        meet = f'{start_meet.isoformat(timespec="minutes")} - {stop_meet.isoformat(timespec="minutes")}'
        if meet in self.meeting:
            ind_start, ind_stop = self.get_indexes(start_meet, stop_meet)
            self.pool[ind_start:ind_stop] *= 0
            self.meeting.pop(meet)
            return 'Встреча удалена'
        return 'Такой встречи нет в списке'

    def is_valid_time(self, start_meet: datetime.time, stop_meet: datetime.time):
        if start_meet < self.start or stop_meet > self.stop:
            return False
        return True



