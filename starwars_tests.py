import pytest
import requests
import jsonschema
import dpath.util
import locators
import starwars_funcs

'''
Task: create test which checks length of array of all people 
with "count" field in response of simple get /people request
'''


def test_all_people(get_list_of_people):
    list_of_found_people = get_list_of_people
    response_just_people = starwars_funcs.give_me_json(locators.links.LINK_TO_PEOPLE)

    count_all_people = len(list_of_found_people)
    count_simple_people = response_just_people["count"]

    assert count_all_people == count_simple_people, f'Count all people = {count_all_people}, ' \
                                                    f'but value "count" for simple "people/" ' \
                                                    f'response = {count_simple_people}'


'''
Task: create test which checks that names of all people are unique
'''


def test_uniq_name(get_list_of_people):
    list_of_found_people = get_list_of_people
    count_people = len(list_of_found_people)

    uniq_name = set(dpath.util.values(list_of_found_people, '*/name'))
    count_uniq_names = len(uniq_name)

    assert count_people == count_uniq_names, f"{count_uniq_names} unique names were found, " \
                                             f"but {count_people} people"


'''
Task: create test which will validate that there is no page with number 0 for people request 
'''


def test_search_zero():
    response = requests.get(f'{locators.links.LINK_TO_PEOPLE}0/')

    assert response.status_code == 404, f'when searching for a zero person status code = {response}'


'''
Task: create test which will validate that all people objects contain required schema fields


Actually, following the documentation, this test should fall, 
because the documentation contains a link to the schema like https://swapi.dev/api/people/schema/, 
but in this form, GET request returns the status 404. 
Correct link: https://swapi.dev/api/people/schema (without the last one /)

But it is also probably that test is expected to fall for this task, 
in which case, it is worth uncommenting the line 4
'''


def test_schema_of_people(get_list_of_people, found_people_schema):
    list_of_found_people = get_list_of_people
    people_schema = found_people_schema
    # people_schema = starwars_func.give_me_json(links.WRONG_LINK_TO_SCHEMA)
    other_people = []

    for i in range(len(list_of_found_people)):
        try:
            jsonschema.validate(list_of_found_people[i], people_schema)
        except jsonschema.exceptions.ValidationError:
            other_people.append(i)
            continue
    assert len(other_people) == 0, f"Not all people match the scheme: {other_people}"


'''
Task: create parametrized test which will check that there are 
3 Skywalker's, 1 Vader, 2 Darth's (using ?search)
'''


@pytest.mark.parametrize('count, search_parameter', [(3, 'Skywalker'), (1, 'Vader'), (2, 'Darth')])
def test_parametrized_search(count, search_parameter):
    link = f'links.LINK_TO_SEARCH{search_parameter}'
    count_result = starwars_funcs.give_me_json(link)['count']

    assert count_result == count, f'{count_result} results found, {count} results expected'


'''
Task: create a few tests for validation that search for people is case insensitive

This was implemented through parameterize, because in my opinion, this method is quite 
convenient for this test, since it allows to add any number of search parameters
'''


@pytest.mark.parametrize('case_insensitive', [(['r2-d2', 'r2-D2', 'R2-d2', 'R2-D2']), (['C3', 'c3']),
                                              (['DARTH', 'DaRtH', 'dArTh'])])
def test_search_is_case_insensitive(case_insensitive):
    response = []
    count_same = 0
    for i in range(len(case_insensitive)):
        link = f'links.LINK_TO_SEARCH{case_insensitive[i]}'
        response.append(starwars_funcs.give_me_json(link))
        if i > 0:
            if response[i] == response[i - 1]:
                count_same += 1

    assert len(response) - 1 == count_same, f'Found {len(response)} records, ' \
                                            f'{count_same + 1} of them are the same'


'''
Task: make sure that the numbers of all the people found are consecutive


Fall is expected, cause there is no person with the number 17 in DB
'''


@pytest.mark.xfail
def test_numbers_going_in_row(get_list_of_people):
    count_people = []

    for i in range(len(get_list_of_people)):
        url = get_list_of_people[i]['url']
        if url.split('/')[-2] != i:
            count_people.append(i)
        i += 1

    assert len(count_people) == 0, f'Missing people with numbers: {count_people}'


'''
Task: create test which will check that search for any char in English alphabet or 
any number from 0 to 9 will return number of results >0 
except cases of search by 6, 9 and 0. 
It is not allowed to use loops inside the test body
'''


@pytest.mark.parametrize('param', locators.params.paramters)
def test_link(param):
    exception = [0, 6, 9]
    link = f'{locators.links.LINK_TO_SEARCH}{param}'
    response_searching = starwars_funcs.give_me_json(link)

    if param in exception and response_searching['count'] == 0:
        pytest.xfail(f'Its {param} inside, so fall is expected')
    assert response_searching['count'] != 0, f"For parameter {param} wasn't found any results"
