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

def drop_day(date): # WARN: this has to be iterated
    return date-timedelta(days=1)

# SCHEDULE = dict(
#         sorted(
#             {
#                 priest.lastname:list(set([
#                     (
#                         date.date,
#                         date.reqested,
#                         ) if date.priest == priest else None\
#                             for date in SortedStipends.query.filter(
#                                 SortedStipends.priest is priest
#                                 ).order_by(
#                                     SortedStipends.date.asc()
#                                     )
#                                 ])) for priest in Priest.query.all()
#                 }.items(), key=lambda x:len(x[1])
#                 # }.items(), key=lambda x:len(list(set(x[1])))
#             )
#         )
# TODO: make a testing function that will print the data in SCHEDULE

def build_schedule() -> dict:
    schedule = {}    
    # find the available days per priest
    priests = [priest.lastname for priest in Priest.query.all()]
    for priest in priests:
        stipends = []
        for date in SortedStipends.query.filter(
                SortedStipends.priest is priest
                ).order_by(
                        SortedStipends.date.asc()
                        ):
            if date.date >= target() and date.requested is not False:
                stipends.append((date.date, date.requested))
            else:
                pass
        schedule[priest] = stipends 
    return dict(sorted(schedule, key=lambda x:len(x[1])))

SCHEDULE = None

def list_of_priests() -> list:
    return [priest for priest in SCHEDULE.keys()]

def free_priest():
    return SCHEDULE.keys()[0]


# date_list = [
#         (date.req_date, date.priest) for date in SortedStipends.query.order_by(
#             SortedStipends.date.asc()
#             )
#         ]
# for priest in SCHEDULE.keys(): # perhaps there is a better way?
#     for item in date_list:
#         if item[1] == priest:
#             if item[0] >= target(): # assumes that the next two weeks are full
#                 pass
#             else:
#                 SCHEDULE[priest]['dates'].append(item[0])
# def list_of_priests() -> list:
#     """Returns a list of priests represented by number of available days
#     """
#     priest_list = []
#     for priest in SCHEDULE.keys():
#         priest_list.append(SCHEDULE[priest]['total'])
#     return priest_list
# def free_priest() -> str:
#     """Find the index of the most available priest
#     """
#     return SCHEDULE.keys()[list_of_priests().index(min(list_of_priests()))]

def assign(mass: list) -> list:
    """Assign the Masses to the priests or days
       Order of priority:
           1. date requested   -> always honored
           2. priest requested -> often honored
           3. date submitted
        Make sure that there are no alterations within two weeks.
        Our data in a list is ordered:
            ["priest", "date"]
    """
    fixed = []
    # the_priest,the_date = mass[0],mass[1]
    the_priest = mass[0]
    the_date = mass[1]
    priests = list_of_priests()
    while len(fixed) < 2:
        tar = target()
        if the_priest is None:
            # NOTE: assuming that the priest is not requested...
            if the_date is not None: # requested date...
                # NOTE: for this to matter we have to have very fixed days...
                for priest in SCHEDULE.keys():
                    if the_date not in SCHEDULE[priest]:
                        # TODO: need a function that will see if the date is fixed
                        fixed = [priest, the_date]
                    else:
                        # FIXME: we have to look on both sides of the date
                        the_date = add_day(the_date) # is this necessary?
            elif the_date is None: # no requested date...
                if tar not in SCHEDULE[free_priest()]['dates']:
                    fixed[1] = tar
                else:
                    for priest in priests.remove(free_priest()):
                        if tar not in SCHEDULE[priest]['dates']:
                            fixed[0] = priest
                            break
                        else:
                            tar = add_day(tar)
            else:
                pass
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
