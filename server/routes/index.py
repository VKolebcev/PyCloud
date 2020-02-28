from server import app
import flask
import xml.etree.ElementTree as etree


def parseXML(xmlfile):
    # create element tree object
    tree = etree.parse(xmlfile)

    # get root element
    root = tree.getroot()

    # create empty list for news items
    newsitems = []

    # iterate news items
    for item in root:
        print(item)
        # empty news dictionary
        news = {}

        # iterate child elements of item
        for child in item:
            news[child.tag] = child.text

        newsitems.append(news)

        # return news items list
    return newsitems


@app.route('/')
def hello_world():
    posts = parseXML('server/routes/catalog.xml')

    return flask.render_template('index.html',
                                posts=posts)

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return app.send_static_file('404.html')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return app.send_static_file('500.html')
