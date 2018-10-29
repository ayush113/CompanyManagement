from django.db import connection
from projects.utils import namedtuplefetchall


def splitandreturn(variable):

    result = []
    res = {}
    for i in variable:
        id = i.project_id
        with connection.cursor() as curr:
            curr.execute("SELECT project_name FROM project where project_id=%s",[id])
            name = namedtuplefetchall(curr)
        string = i.bill
        values = string.split(',')
        amount = values[0]
        amount = amount.split(':')
        amount = int(amount[1])
        res['amount'] = amount
        breakdown = values[1]
        breakdown = breakdown.split('/')
        size = len(breakdown)
        li = []
        for i in range(size):
            if (i == 0):
                temp = breakdown[i].split('{')
                li.append(temp[1])
            elif i == size - 1:
                temp = breakdown[i].split('}')
                li.append(temp[0])
            else:
                li.append(breakdown[i])
        res['breakdown'] = li
        res['name'] = name[0].project_name
        result.append(res)
        res = dict()
    return result

