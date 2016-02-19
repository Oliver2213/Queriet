# API wrapper for urban dictionary
# By Blake Oliver <oliver22213@me.com>

import requests

api_endpoint = 'http://api.urbandictionary.com/v0/define'


def define(term):
    """Searches urban dictionary for the provided term, returning a list of 'UrbanDictResult' objects, with information for each result in each object."""
    r = requests.get(api_endpoint, params={'term': term})
    # We extract the json separately so as to catch any ValueErrors
    try:
        urbjson = r.json()
    except ValueError as e:
        raise UrbanDictionaryParseError(
            "Error parsing json response. %s" % (e))
    try:
        results = parse(urbjson)
    except KeyError as e:
        raise UrbanDictionaryResultParseError(
            "Error parsing result: %s." % (e))
    return results


def parse(urbjson):
    """Parse an urban dictionary json response and create a list of the results, then return them."""
    res = []
    for entry in urbjson['list']:
        itm = UrbanDictionaryResult(
            entry['word'],
            entry['definition'],
            entry['permalink'],
            entry['defid'],
            entry['thumbs_up'],
            entry['thumbs_down'],
            entry['author'],
            entry['example'])
        res.append(itm)
    return res


class UrbanDictionaryResult(object):
    """A standard result object for an urban dictionary entry"""

    def __init__(
            self,
            term,
            definition,
            permalink,
            id,
            thumbs_up,
            thumbs_down,
            author,
            example=None):
        self.term = term
        self.definition = definition
        self.example = example
        self.permalink = permalink
        self.id = id
        self.thumbs_up = thumbs_up
        self.thumbs_down = thumbs_down
        self.author = author


class UrbanDictionaryParseError(Exception):
    pass


class UrbanDictionaryResultParseError(Exception):
    pass
