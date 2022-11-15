import datetime

from workers import Employee
from utilites.get_free_time import get_common_free_time


class EmployeeTestVarint(Employee):
    def __init__(self, start_work, stop_work, first_name='Иван', patronymic='Иванович', last_name='Иванов',
                 date_birth=datetime.date(1754, 10, 10), gender='mail', post='dev', salary=100,
                 work_experience_company=1, email=None):

        Employee.__init__(self, first_name=first_name, patronymic=patronymic, last_name=last_name,
                          date_birth=date_birth, gender=gender, post=post, salary=salary,
                          email=email, start_work=start_work, stop_work=stop_work)


def test_employ():
    e = EmployeeTestVarint(email='zorokon@yandex.ru', start_work=datetime.time(10, 0), stop_work=datetime.time(19, 0))
    # e('zorokon@yandex.ru', passwd='*********') - можно отправить письмо, правда сейчас только через yandex

    assert e.salary == 100
    e.salary = 200
    assert e.salary == 200


def test_wh_get_working_hours():
    e1 = EmployeeTestVarint(start_work=datetime.time(10, 0), stop_work=datetime.time(19, 0))
    e2 = EmployeeTestVarint(start_work=datetime.time(0, 24), stop_work=datetime.time(3, 5))

    assert e1.working_hours.get_working_hours() == 'Working: 10:00 - 19:00'
    assert e2.working_hours.get_working_hours() == 'Working: 00:24 - 03:05'


def test_get_get_free_time():
    e1 = EmployeeTestVarint(start_work=datetime.time(0, 0), stop_work=datetime.time(8, 0))
    e2 = EmployeeTestVarint(start_work=datetime.time(4, 0), stop_work=datetime.time(12, 0))
    e3 = EmployeeTestVarint(start_work=datetime.time(0, 0), stop_work=datetime.time(12, 0))
    e4 = EmployeeTestVarint(start_work=datetime.time(4, 0), stop_work=datetime.time(16, 0))

    e1.working_hours.add_meeting(datetime.time(4, 20), datetime.time(6, 0))
    assert e1.working_hours.get_free_time() == ['00:00 - 04:19', '06:00 - 07:59']

    e2.working_hours.add_meeting(datetime.time(5, 30), datetime.time(6, 30))
    e2.working_hours.add_meeting(datetime.time(8, 20), datetime.time(10, 0))
    assert e2.working_hours.get_free_time() == ['04:00 - 05:29', '06:30 - 08:19', '10:00 - 11:59']

    assert get_common_free_time([]) is None
    assert get_common_free_time((e1,)) == ['00:00 - 04:19', '06:00 - 07:59']
    assert get_common_free_time((e1, e2)) == ['04:00 - 04:19', '06:30 - 07:59']

    e3.working_hours.add_meeting(datetime.time(2, 20), datetime.time(4, 10))
    e3.working_hours.add_meeting(datetime.time(6, 0), datetime.time(7, 0))
    assert e3.working_hours.get_free_time() == ['00:00 - 02:19', '04:10 - 05:59', '07:00 - 11:59']

    e4.working_hours.add_meeting(datetime.time(5, 15), datetime.time(6, 0))
    e4.working_hours.add_meeting(datetime.time(8, 0), datetime.time(9, 0))
    assert e4.working_hours.get_free_time() == ['04:00 - 05:14', '06:00 - 07:59', '09:00 - 15:59']

    assert get_common_free_time((e1, e2, e3, e4)) == ['04:10 - 04:19', '07:00 - 07:59']


def test_add_del_meet():
    e = EmployeeTestVarint(start_work=datetime.time(8, 0), stop_work=datetime.time(17, 0))

    assert e.working_hours.add_meeting(datetime.time(4, 0), datetime.time(6, 0)) == 'Время не подходит'
    assert e.working_hours.add_meeting(datetime.time(9, 0), datetime.time(18, 0)) == 'Время не подходит'
    assert e.working_hours.add_meeting(datetime.time(9, 0), datetime.time(11, 0)) == 'Встреча добавлена'
    assert e.working_hours.add_meeting(datetime.time(9, 0), datetime.time(11, 0)) == 'Время полностью занято'
    assert e.working_hours.add_meeting(datetime.time(8, 30), datetime.time(11, 0)) == 'Время частично занято'
    assert e.working_hours.get_free_time() == ['08:00 - 08:59', '11:00 - 16:59']

    assert e.working_hours.del_meeting(datetime.time(10, 0), datetime.time(11, 0)) == 'Такой встречи нет в списке'
    assert e.working_hours.del_meeting(datetime.time(9, 0), datetime.time(11, 0)) == 'Встреча удалена'
    assert e.working_hours.get_free_time() == ['08:00 - 16:59']
