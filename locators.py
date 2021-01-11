import string


class links:
    LINK_TO_PEOPLE = 'https://swapi.dev/api/people/'
    LINK_TO_SEARCH = 'https://swapi.dev/api/people/?search='
    LINK_TO_SCHEMA = 'https://swapi.dev/api/people/schema'
    WRONG_LINK_TO_SCHEMA = 'https://swapi.dev/api/people/schema/'


class params:
    paramters = tuple(list(range(10)) + list(string.ascii_lowercase[:26]))
