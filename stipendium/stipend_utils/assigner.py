from datetime import datetime
from datetime import timedelta
# from stipendium import app
# from stipendium import db
# from stipendium.models import Center
from stipendium.models import Priest
from stipendium.models import Queue
from stipendium.models import SortedStipends


# TODO: give Gregorian capabilities
# TODO: check for shortages in the upcoming week

def target():
    return datetime.today()+timedelta(weeks=2)

def add_day(date):
    return date+timedelta(days=1)

# The total in SCHEDULE is necessary to find which priest
# has the most free schedule
SCHEDULE = {
        priest.lastname:{
            'dates':[], # fill with date_list below
            'total': SortedStipends.query.filter(
                SortedStipends.priest == priest
                ).count(), # WARN: same as number of dates, plus the current
            } for priest in Priest.query.all()
        }
# for i, priest in enumerate(SCHEDULE.keys()):
#     SCHEDULE[priest]['total'] = SortedStipends.query.filter(
#             SortedStipends.priest == priest
#             ).count()
date_list = [
        (date.req_date, date.priest) for date in SortedStipends.query.order_by(
            SortedStipends.date.asc()
            )
        ]
for priest in SCHEDULE.keys(): # perhaps there is a better way?
    for item in date_list:
        if item[1] == priest:
            if item[0] >= target(): # assumes that the next two weeks are full
                pass
            else:
                SCHEDULE[priest]['dates'].append(item[0])

def list_of_priests() -> list:
    """Returns a list of priests represented by number of available days
    """
    priest_list = []
    for priest in SCHEDULE.keys():
        priest_list.append(SCHEDULE[priest]['total'])
    return priest_list

def free_priest() -> str:
    """Find the index of the most available priest
    """
    return SCHEDULE.keys()[list_of_priests().index(min(list_of_priests()))]

def assign(mass: list) -> list:
    """Assign the Masses to the priests or days
       Order of priority:
           1. date requested
           2. priest requested
           3. date submitted
        Make sure that there are no alterations within two weeks.
        Our data in a list is ordered: ["priest", "date"]
    """
    fixed = []
    # the_priest,the_date = mass[0],mass[1]
    the_date = mass[1]
    while len(fixed) > 2:
        tar = target()
        if the_date is not None: # requested date...
            if the_date not in SCHEDULE[free_priest()]['dates']:
                fixed[1] = the_date
            else:
                for priest in list_of_priests().remove(free_priest()):
                    if the_date not in SCHEDULE[priest]['dates']:
                        fixed[0] = priest
                        break
                else:
                    the_date = add_day(the_date) # is this necessary?
        elif the_date is None: # no requested date...
            if tar not in SCHEDULE[free_priest()]['dates']:
                fixed[1] = tar
            else:
                for priest in list_of_priests().remove(free_priest()):
                    if tar not in SCHEDULE[priest]['dates']:
                        fixed[0] = priest
                        break
                    else:
                        tar = add_day(tar)
        else:
            pass
    return fixed


def sort_stipends() -> None:
    stipends = Queue.query.order_by(Queue.accepted.asc())
    for stipend in stipends:
        assignment = assign([stipend.priest, stipend.req_date])
        for x in range(1,stipend.masses+1):
            single_stipend = SortedStipends(
                    queue_id = stipend.id,
                    priest = assignment[0],
                    date = assignment[1],
                    amount = stipend.amount/stipend.masses,
                    )
