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
    index = 1
    # iterate news items
    for item in root:
        # empty news dictionary
        news = {}
        news["id"] = index
        # iterate child elements of item
        for child in item:
            news[child.tag] = child.text
        index += 1

        try:
            int(list(news.values())[1])
        except ValueError:
            newsitems.append(news)
        except TypeError:
            pass

        # return news items list
    return newsitems


def delete_item(path, id):
    tree = etree.parse(path)
    root = tree.getroot()
    counter = 1
    # ‭ ‬удаляем один подэлемент
    for item in root:
        if counter == int(id):
            for child in item:
                item.remove(child)

        counter += 1

    # ‭ ‬создаём новый файл XML с результатами
    tree.write(path)


def add_item(path, item):
    tree = etree.parse(path)
    root = tree.getroot()
    child = etree.Element("service")
    name = etree.SubElement(child, "name")
    cost = etree.SubElement(child, "cost")
    description = etree.SubElement(child, "description")
    name.text = item["name"]
    cost.text = item["cost"]
    description.text = item["description"]

    root.append(child)

    # ‭ ‬создаём новый файл XML с результатами
    tree.write(path)


@app.route('/')
def hello_world():
    posts = parseXML('server/routes/catalog.xml')

    return flask.render_template('index.html', posts=posts)


@app.route("/forward/", methods=['POST'])
def delete():
    delete_item('server/routes/catalog.xml', list(flask.request.form.to_dict().keys())[0])
    posts = parseXML('server/routes/catalog.xml')

    return flask.redirect(flask.url_for('hello_world'))


@app.route("/add/", methods=['POST'])
def add():
    print(flask.request.form.to_dict())
    add_item('server/routes/catalog.xml', flask.request.form.to_dict())
    posts = parseXML('server/routes/catalog.xml')

    return flask.redirect(flask.url_for('hello_world'))


@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return app.send_static_file('404.html')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return app.send_static_file('500.html')
