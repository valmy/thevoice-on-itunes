import os
import jinja2
import webapp2
from chart import Chart
from google.appengine.ext import ndb
import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

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
        day_chart = DayChart(id='{}/{}'.format(country, date.strftime('%Y/%m/%d')), date=date, country=country)
        day_chart_key = day_chart.put()
        chart = Chart(country)
        results = chart.read(date.strftime('%Y/%m/%d'))
        for result in results:
            entry = Entry(rank=result['rank'], artist=result['artist'], song=result['song'], parent=day_chart_key)
            entry_key = entry.put()
            entries.append(entry)
    else:
        day_chart_key = day_chart.key
        query = Entry.query(ancestor=day_chart.key).order(Entry.rank)
        entries = query.fetch(100)
    return (day_chart, entries)

class MainPage(webapp2.RequestHandler):

    def get(self):
        today = date=datetime.date(2013, 5, 22)

        (day_chart, entries) = entries_by_date('us', today)

        template_values = { 'day_chart': day_chart, 'entries': entries }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class UsaDatePage(webapp2.RequestHandler):

    def get(self, year, month, day):
        today = date=datetime.date(int(year), int(month), int(day))

        (day_chart, entries) = entries_by_date('us', today)

        template_values = { 'day_chart': day_chart, 'entries': entries }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class AustralianPage(webapp2.RequestHandler):

    def get(self):
        today = date=datetime.date(2013, 5, 22)

        (day_chart, entries) = entries_by_date('aus', today)

        template_values = { 'day_chart': day_chart, 'entries': entries }
        template = JINJA_ENVIRONMENT.get_template('aus.html')
        self.response.write(template.render(template_values))

class AustralianDatePage(webapp2.RequestHandler):

    def get(self, year, month, day):
        today = date=datetime.date(int(year), int(month), int(day))

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
