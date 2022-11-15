import numpy as np
from typing import Union

from workers import WorkingHoursFreeTime


def get_common_free_time(sequence: Union[list, tuple]):
    """Prerequisite: the dimension of the arrays of workers' working hours must all be
    the same. The bottom line: we put all the arrays into one in numpy and iterate the resulting array
    once. Cells in which 0 is the total free time."""
    if not sequence:
        return None
    else:
        if len(sequence) == 1:
            return sequence[0].working_hours.get_free_time()
        else:
            common_pool = np.array([employee.working_hours.pool for employee in sequence])
            common_pool = np.sum(common_pool, axis=0)  # in one line
            step = sequence[0].working_hours.step  # minutes
            wh = WorkingHoursFreeTime(step=step, pool=common_pool)
            common_free_time = wh.get_free_time()
            return common_free_time

