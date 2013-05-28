import os
import jinja2
import webapp2
from chart import Chart

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class MainPage(webapp2.RequestHandler):

    def get(self):
        chart = Chart('us')
        results = chart.read('2013/05/21')
        template_values = { 'results': results }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class UsaDatePage(webapp2.RequestHandler):

    def get(self, year, month, day):
        chart = Chart('us')
        results = chart.read('{}/{}/{}'.format(year, month, day))
        template_values = { 'results': results }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class AustralianPage(webapp2.RequestHandler):

    def get(self):
        chart = Chart('aus')
        results = chart.read('2013/05/21')
        template_values = { 'results': results }
        template = JINJA_ENVIRONMENT.get_template('aus.html')
        self.response.write(template.render(template_values))

class AustralianDatePage(webapp2.RequestHandler):

    def get(self, year, month, day):
        chart = Chart('aus')
        results = chart.read('{}/{}/{}'.format(year, month, day))
        template_values = { 'results': results }
        template = JINJA_ENVIRONMENT.get_template('aus.html')
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/(.{4})/(.{2})/(.{2})', UsaDatePage),
    ('/aus', AustralianPage),
    ('/aus/(.{4})/(.{2})/(.{2})', AustralianDatePage)
], debug=True)
