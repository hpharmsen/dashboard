import os

from sources.googlesheet import sheet_tab, sheet_value
from model.caching import reportz
from model.trendline import trends
from sources.simplicate import simplicate


def to_int(s):
    if type(s) == int:
        return s
    return int(s.replace('€ ', '').replace('.', '').replace('%', ''))


def is_int(s):
    try:
        to_int(s)
        return True
    except:
        return False


#@reportz(hours=24)
def sales_waarde():
    res = sum([s['value'] for s in open_sales()])
    trends.update('sales_waarde', res)
    return res


def format_project_name(line, maxlen):
    name = line['organization'].split()[0] + ' - ' + line['subject']
    if len(name) > maxlen:
        name = name[: maxlen - 1] + '..'
    return name


@reportz(hours=24)
def sales_waarde_details():
    tab = sheet_tab('Sales - force', 'Kansen')
    data_rows = []
    for row in tab[3:]:
        if not is_int(row[2]):
            row[2] = 0
        if is_int(row[5]) and 0 < to_int(row[5]) < 60:
            data_rows += [row[:2] + [to_int(row[2])] + [to_int(row[3])] + [row[4]] + [to_int(row[6])] + [row[13]]]

    # data_rows = [
    #    row[:2] + [to_int(row[2])] + [to_int(row[3])] + [row[4]] + [to_int(row[6])] + [row[13]]
    #    for row in tab[3:]
    #    if is_int(row[5]) and 0 < to_int(row[5]) < 60
    # ]
    return data_rows


def top_x_sales(number=3):
    top = sorted(open_sales(), key=lambda a: -a['value'])[:number]
    return [[format_project_name(a, 40), a['value']] for a in top]

def open_sales():
    sim = simplicate()
    return [s for s in sim.sales_flat() if 5 <= s['progress_position'] <=7]


@reportz(hours=24)
def werk_in_pijplijn():
    tab = sheet_tab('Sales - force', 'Kansen')
    res = to_int(sheet_value(tab, 2, 9))
    trends.update('werk_in_pijplijn', res)
    return res


@reportz(hours=24)
def werk_in_pijplijn_details():
    tab = sheet_tab('Sales - force', 'Kansen')
    data_rows = [
        row[:2] + [to_int(row[7])] + [to_int(row[8])] + [row[9]]
        for row in tab[3:]
        if is_int(row[8]) and to_int(row[8]) > 0
    ]
    return data_rows

if __name__=='__main__':
    os.chdir('..')
    for s in top_x_sales(5):
        print( s )
    print( sales_waarde())


