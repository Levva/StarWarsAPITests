import pytest
import json
import requests
import starwars_funcs
from locators import links

'''
Task: create fixture which will return the array of all people


Despite the fact that there is a special function for getting JSON,
it is more convenient to use a simple query and convert to 
the desired format, since the numbers of specific people is not
serial
'''


@pytest.fixture()
def get_list_of_people():
    i, j = 1, 0
    list_of_all_people = {}

    while True:
        answer = requests.get(f'{links.LINK_TO_PEOPLE}{i}')
        if answer.ok:
            list_of_all_people[j] = json.loads(answer.text)
            i += 1
            j += 1
        else:
            answer = requests.get(f'{links.LINK_TO_PEOPLE}{i + 1}')
            if answer.ok:
                list_of_all_people[j] = json.loads(answer.text)
                i += 2
                j += 1
            else:
                break

    return list_of_all_people


'''
Task: create fixture which will return schema of people object
'''


@pytest.fixture()
def found_people_schema():
    return starwars_funcs.give_me_json(links.LINK_TO_SCHEMA)


'''
Task: create factory fixture which will return search people results
'''


@pytest.fixture
def some_factory_for_searching():
    def _some_factory_for_searching(link):
        return {'response': starwars_funcs.give_me_json(link)}

    return _some_factory_for_searching
