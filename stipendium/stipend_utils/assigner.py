from datetime import datetime
from datetime import timedelta
# from stipendium import app
# from stipendium import db
# from stipendium.models import Center
from stipendium.models import Priest
from stipendium.models import Queue
from stipendium.models import SortedStipends



TARGET = datetime.today()+timedelta(weeks=2)

def iterate_target():
    TARGET+timedelta(days=1)
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
            SCHEDULE[priest]["dates"].append(item[0])

def list_of_priests() -> list:
    priest_list = []
    for priest in SCHEDULE.keys():
        priest_list.append(SCHEDULE[priest_list]['total'])
    return priest_list

def least_common_priest() -> str:
    return SCHEDULE.keys()[list_of_priests().index(max(list_of_priests()))]

# TODO figure something out so that the Masses can only be scheduled for the next week.

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
    # NOTE: All of this assumes that we are not replacing dates
    while len(fixed) > 2:
        if the_date is not None:
            if the_date not in SCHEDULE[least_common_priest()]['dates']:
                fixed[1] = the_date
            else:
                for priest in list_of_priests().remove(least_common_priest()):
                    if the_date not in SCHEDULE[priest]['dates']:
                        fixed[0] = priest
                        break
                else:
                    the_date = iterate_date()
        elif the_date is None:
            if TARGET not in SCHEDULE[least_common_priest()]['dates']:
                fixed[1] = TARGET
            else:
                for priest in list_of_priests().remove(least_common_priest()):
                    if TARGET not in SCHEDULE[priest]['dates']:
                        fixed[0] = priest
                        break
                    else:
                        TARGET = iterate_target()
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
