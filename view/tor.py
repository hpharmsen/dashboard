import os
from layout.basic_layout import headersize, midsize, defsize
from layout.block import Block, VBlock, HBlock, TextBlock, Table, Page
from layout.chart import StackedBarChart
from model.tor import tor_projecten, tor_total_budget, tor_total_spent, tor_perc_spent, tor_facturen, tor_per_maand


def render_tor_page():

    kengetallen = Block()
    kengetallen.add_absolute_block(0, 0, TextBlock('Totaal budget', defsize, color='gray'))
    kengetallen.add_absolute_block(0, 70, TextBlock('Besteed budget', defsize, color='gray'))
    kengetallen.add_absolute_block(190, 0, TextBlock(tor_total_budget(), midsize, format='K'))
    kengetallen.add_absolute_block(190, 60, TextBlock(tor_total_spent(), midsize, format='K'))
    kengetallen.height = 100  # Nodig omdat een blok met alleen maar abs elementen erin zelf geen hoogte heeft
    kengetallen.width = 300  # Nodig omdat een blokvan 0 breed nog steeds geen ruimte in neemt

    projectoverzicht = VBlock(
        [
            TextBlock('Projectoverzicht', midsize),
            Table(
                tor_projecten(),
                headers=['id', 'title', 'Budget', 'Uren', 'Besteed', 'Percentage besteed'],
                aligns=['left', 'left', 'right', 'right', 'right', 'right'],
                formats=['', '', '€', '0', '€', '%'],
                totals=[0, 0, 1, 1, 1, 0],
                row_linking=lambda l, v: f'https://oberview.oberon.nl/project/{v[0]}',
            ),
        ]
    )
    tp = tor_projecten().values.tolist()
    besteed = [min(t[4], t[2]) for t in tp]
    beschikbaar = [max(0, t[2] - t[4]) for t in tp]
    overbudget = [max(0, t[4] - t[2]) for t in tp]
    bottom_labels = [t[1] for t in tp]
    chart = VBlock(
        [
            TextBlock('Grafiek', midsize),
            StackedBarChart(
                500,
                440,
                '',
                ['besteed', 'beschikbaar', 'over budget'],
                [besteed, beschikbaar, overbudget],
                ['#55c', '#5c5', '#C55'],
                bottom_label=bottom_labels,
                horizontal=True,
            ),
        ]
    )

    permaand = VBlock(
        [
            TextBlock('Per maand', midsize),
            Table(
                tor_per_maand(),
                headers=['maand', 'uren', 'besteed', 'per partner'],
                aligns=['left', 'right', 'right', 'right'],
                formats=['', 0, '€', '€'],
                totals=[0, 1, 1, 1],
            ),
        ]
    )

    facturen = VBlock(
        [
            TextBlock('Gefactureerd', midsize),
            Table(
                tor_facturen(),
                headers=['factuur', 'datum', 'bedrag', 'status'],
                aligns=['left', 'left', 'right', 'left'],
                formats=['', '', '€', ''],
                totals=[0, 0, 1, 0],
            ),
        ]
    )

    row1 = HBlock([projectoverzicht, chart])
    row2 = HBlock([permaand, facturen])

    page = Page([TextBlock('TOR 3', headersize), VBlock([row1, row2])])

    page.render('output/tor.html')
    page.render('output/limited/tor.html', limited=1)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(__file__)))
    render_tor_page()
