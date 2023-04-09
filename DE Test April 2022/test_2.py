import json
import requests as req
# A team of analysts wish to discover how far people are travelling to their nearest
# desired court. We have provided you with a small test dataset so you can find out if
# it is possible to give the analysts the data they need to do this. The data is in
# `people.csv` and contains the following columns:
# - person_name
# - home_postcode
# - looking_for_court_type

# The courts and tribunals finder API returns a list of the 10 nearest courts to a
# given postcode. The output is an array of objects in JSON format. The API is
# accessed by including the postcode of interest in a URL. For example, accessing
# https://courttribunalfinder.service.gov.uk/search/results.json?postcode=E144PU gives
# the 10 nearest courts to the postcode E14 4PU. Visit the link to see an example of
# the output.

# Below is the first element of the JSON array from the above API call. We only want the
# following keys from the json:
# - name
# - dx_number
# - distance
# dx_number is not always returned and the "types" field can be empty.

"""
[
    {
        "name": "Central London Employment Tribunal",
        "lat": 51.5158158439741,
        "lon": -0.118745425821452,
        "number": null,
        "cci_code": null,
        "magistrate_code": null,
        "slug": "central-london-employment-tribunal",
        "types": [
            "Tribunal"
        ],
        "address": {
            "address_lines": [
                "Victory House",
                "30-34 Kingsway"
            ],
            "postcode": "WC2B 6EX",
            "town": "London",
            "type": "Visiting"
        },
        "areas_of_law": [
            {
                "name": "Employment",
                "external_link": "https%3A//www.gov.uk/courts-tribunals/employment-tribunal",
                "display_url": "<bound method AreaOfLaw.display_url of <AreaOfLaw: Employment>>",
                "external_link_desc": "Information about the Employment Tribunal"
            }
        ],
        "displayed": true,
        "hide_aols": false,
        "dx_number": "141420 Bloomsbury 7",
        "distance": 1.29
    },
    etc
]
"""

# Use this API and the data in people.csv to determine how far each person's nearest
# desired court is. Generate an output (of whatever format you feel is appropriate)
# showing, for each person:
# - name
# - type of court desired
# - home postcode
# - nearest court of the right type
# - the dx_number (if available) of the nearest court of the right type
# - the distance to the nearest court of the right type


def get_people_info(file_name: str) -> list[dict]:
    '''Retrieves all people's info from csv file with format
    "name", "home_postcode", and "looking_for_court_type"
    '''
    people_info = []
    with open(file_name) as data:
        next(data)
        for line in data:
            person = {}
            individual_data = line.split(",")
            person["name"] = individual_data[0].strip()
            person["home_postcode"] = individual_data[1].strip()
            person["looking_for_court_type"] = individual_data[2].strip()
            people_info.append(person)
    return people_info


def get_court_api_info(postcode: str) -> json:
    '''Retrieves all data from API from the specified postcode'''
    url = f"https://courttribunalfinder.service.gov.uk/search/results.json?postcode={postcode}"
    response = req.get(url, timeout=5)
    court_data = response.json()
    if len(court_data) < 1:
        raise ValueError(
            "No courts found for that postcode, check if correct postcode")
    return court_data


def get_closest_correct_court(court_json: list[dict], court_type) -> dict:
    '''Retrieves to closest court with correct typing from the json data
    extracted from the API
    '''
    correct_court_type = [
        court for court in court_json if court_type in court["types"]]
    if len(correct_court_type) < 1:
        raise ValueError("No courts found with desired type")
    min_distance_court = correct_court_type[0]
    min_distance = min_distance_court["distance"]
    for court in correct_court_type:
        if court["distance"] < min_distance:
            min_distance = court["distance"]
            min_distance_court = court
    return min_distance_court


def combine_person_with_court(person: dict, correct_court: dict) -> dict:
    '''Combines a person with their closest court and returns this in
    one dict
    '''
    person["nearest_court_of_right_type"] = correct_court["name"]
    if correct_court["dx_number"] is not None:
        person["dx_number"] = correct_court["dx_number"]
    person["distance_to_court"] = correct_court["distance"]
    return person


def find_correct_courts_for_people(people: list[dict]) -> list[dict]:
    '''Takes a list of people and returns the closest desired court 
    for each of them'''
    courts_found = []
    for person in people:
        courts = get_court_api_info(person["home_postcode"])
        correct_court = get_closest_correct_court(
            courts, person["looking_for_court_type"])
        final_person = combine_person_with_court(person, correct_court)
        courts_found.append(final_person)
    return courts_found


if __name__ == "__main__":
    # [TODO]: write your answer here
    people_main = get_people_info("people.csv")

    print(find_correct_courts_for_people(people_main))
