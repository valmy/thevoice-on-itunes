import os
import jinja2
import webapp2
from chart import Chart
from google.appengine.ext import ndb
import datetime
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
#    extensions=['jinja2.ext.autoescape'])

class DayChart(ndb.Model):
    """ Ranking results of a day """
    date = ndb.DateProperty()
    country = ndb.StringProperty()

class Entry(ndb.Model):
    """ Song entry """
    rank = ndb.IntegerProperty()
    artist = ndb.StringProperty()
    song = ndb.StringProperty()

def entries_by_date(country, date):
    day_chart = DayChart.get_by_id('{}/{}'.format(country, date.strftime('%Y/%m/%d')))
    entries = []

    if day_chart == None:
        chart = Chart(country)
        results = chart.read(date.strftime('%Y/%m/%d'))
        if not results:
            return None
        day_chart = DayChart(id='{}/{}'.format(country, date.strftime('%Y/%m/%d')), date=date, country=country)
        day_chart_key = day_chart.put()

        for result in results:
            entry = Entry(rank=result['rank'], artist=result['artist'], song=result['song'], parent=day_chart_key)
            entry_key = entry.put()
            entries.append(entry)
    else:
        day_chart_key = day_chart.key
        query = Entry.query(ancestor=day_chart.key).order(Entry.rank)
        entries = query.fetch(100)
    return (day_chart, entries)

def query_points(country, limit=14):
    chart_query = DayChart.query(DayChart.country == country).order(-DayChart.date)
    charts = chart_query.fetch(limit)
    songs = []
    ranks = []
    songs.append("Date")
    for i, chart in enumerate(reversed(charts)):
        # songs.append(["'{}'".format(chart.date)])
        r = {}
        r[0] = chart.date.isoformat()
        song_query = Entry.query(ancestor=chart.key)
        for entry in song_query.iter():
            song = '{} - {}'.format(entry.artist.encode('utf-8'), entry.song.encode('utf-8'))
            try:
                idx = songs.index(song)
            except ValueError:
                songs.append(song)
                idx = len(songs) - 1
            r[idx] = 100 - entry.rank + 1
        ranks.append(r)

    table = []
    table.append(songs)
    for j, rank in enumerate(ranks):
        row = []
        for i in range(len(songs)):
            if i == 0:
                row.append(rank.get(0))
            else:
                row.append(rank.get(i, 0))
        table.append(row)
    return json.dumps(table)

class MainPage(webapp2.RequestHandler):

    def get(self):
        today = datetime.date.today() - datetime.timedelta(days=1)

        table = query_points('us', 10)

        template_values = { 'table': table }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class UsaDatePage(webapp2.RequestHandler):

    def get(self, year, month, day):
        today = datetime.date(int(year), int(month), int(day))

        (day_chart, entries) = entries_by_date('us', today)

        template_values = { 'day_chart': day_chart, 'entries': entries }
        template = JINJA_ENVIRONMENT.get_template('us.html')
        self.response.write(template.render(template_values))

class AustralianPage(webapp2.RequestHandler):

    def get(self):
        today = datetime.date.today() - datetime.timedelta(days=1)

        table = query_points('aus', 10)

        template_values = { 'table': table }

        template = JINJA_ENVIRONMENT.get_template('index-aus.html')

        self.response.write(template.render(template_values))

class AustralianDatePage(webapp2.RequestHandler):

    def get(self, year, month, day):
        today = datetime.date(int(year), int(month), int(day))

        (day_chart, entries) = entries_by_date('aus', today)

        template_values = { 'day_chart': day_chart, 'entries': entries }

        template = JINJA_ENVIRONMENT.get_template('aus.html')
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/(.{4})/(.{2})/(.{2})', UsaDatePage),
    ('/aus', AustralianPage),
    ('/aus/(.{4})/(.{2})/(.{2})', AustralianDatePage)
], debug=True)
