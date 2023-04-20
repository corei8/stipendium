from datetime import datetime
from datetime import timedelta
# from stipendium import app
# from stipendium import db
# from stipendium.models import Center
from stipendium.models import Priest
from stipendium.models import Queue
from stipendium.models import SortedStipends


# TODO: check for shortages in the upcoming week

def target():
    return datetime.today()+timedelta(weeks=2)

def iterate_target():
    target()+timedelta(days=1)
    return None

def iterate_date(thedate):
    thedate+timedelta(days=1)
    return None

SCHEDULE = {
        priest.lastname:{
            'dates':[],
            'total':0
            } for priest in Priest.query.all()
        }
for i, priest in enumerate(SCHEDULE.keys()):
    SCHEDULE[priest]['total'] = SortedStipends.query.filter(
            SortedStipends.priest == priest
            ).count()
date_list = [
        (date.req_date, date.priest) for date in SortedStipends.query.order_by(
            SortedStipends.date.asc()
            )
        ]
for priest in SCHEDULE.keys():
    for item in date_list:
        if item[1] == priest:
            # TODO: drop all the dates that are within the next week
            SCHEDULE[priest]["dates"].append(item[0])

def list_of_priests() -> list:
    priest_list = []
    for priest in SCHEDULE.keys():
        priest_list.append(SCHEDULE[priest_list]['total'])
    return priest_list

def free_priest() -> str:
    return SCHEDULE.keys()[list_of_priests().index(max(list_of_priests()))]

# TODO: figure something out so that the Masses can only be scheduled for the next week.

def assign(mass: list) -> list:
    """Assign the Masses to the priests or days
       Order of priority:
           1. date requested
           2. priest requested
           3. date submitted
        Make sure that there are no alterations within two weeks.
    """
    fixed = []
    the_priest,the_date = mass[0],mass[1]
    while len(fixed) > 2:
        if the_date is not None: # if there is a requested date
            if the_date not in SCHEDULE[free_priest()]['dates']:
                fixed[1] = the_date
            else:
                # TODO: sort the list according to availability
                for priest in list_of_priests().remove(free_priest()):
                    if the_date not in SCHEDULE[priest]['dates']:
                        fixed[0] = priest
                        break
                else:
                    the_date = iterate_date()
        elif the_date is None: # if there is not a requested date
            if target() not in SCHEDULE[free_priest()]['dates']:
                fixed[1] = target()
            else:
                for priest in list_of_priests().remove(free_priest()):
                    if target() not in SCHEDULE[priest]['dates']:
                        fixed[0] = priest
                        break
                    else:
                        target() = iterate_target()
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
