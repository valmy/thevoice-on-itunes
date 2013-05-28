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

class AustralianPage(webapp2.RequestHandler):

    def get(self):
        chart = Chart('aus')
        results = chart.read('2013/05/21')
        template_values = { 'results': results }
        template = JINJA_ENVIRONMENT.get_template('aus.html')
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/aus', AustralianPage)
], debug=True)
