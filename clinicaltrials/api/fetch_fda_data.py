""""
Code for collecting data from the FDA API and outputting to a JSON file.
Written by Alison Spencer.
"""

import time
import requests
import json
import pathlib


def make_fda_api_call(skip, limit=1000, start_date="2003-01-01", end_date="2024-02-19"):
    """
    Makes an API call to FDA's Drugs@FDA API.

    Args:
        - skip: (int) value initially sent to 0. used to paginate.
        - limit: (int) the maximum number of results that can be returned from
        each API query. The API sets this to 1000.
        -start_date: (str) the start date of submission_status_date used in
        results. For the project, this is set to the start of 2003 to align with
        the clinical trials data (this is approximately when clinical trials
        data is first available from)
        -end_date: (str) the end date of submission_status_date used in
        results. For the project, this is set to 2/19/2024 to align with our
        final data collection.

    Returns:
        - response.json(): the json file for that specific page and query.
    """

    base_url = "https://api.fda.gov/drug/drugsfda.json?search=submissions.submission_status_date"
    # FDA API has trouble parsing parameters, which is why the url is being input
    # into requests as a string.
    second_part_url = "%5B" + start_date + "%20TO%20" + end_date + "%5D"
    third_part_url = "&skip=" + str(skip) + "&limit=" + str(limit)
    url = base_url + second_part_url + third_part_url
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()


def pull_fda_api_data(
    skip=0, limit=1000, start_date="2003-01-01", end_date="2024-02-19"
):
    """
    Pull data for the given time frame from the Drugs@FDA API.

    Args:
        - skip: (int) value initially sent to 0. used to paginate.
        - limit: (int) the maximum number of results that can be returned from
        each API query. The API sets this to 1000.
        -start_date: (str) the start date of submission_status_date used in
        results. For the project, this is set to the start of 2003 to align with
        the clinical trials data (this is approximately when clinical trials
        data is first available from)
        -end_date: (str) the end date of submission_status_date used in
        results. For the project, this is set to 2/19/2024 to align with our
        final data collection.

    Returns:
        - Writes data from the API out to a json file.
    """

    results = []
    count_results = 0
    next_results = count_results + limit

    while True:
        print(f"Pulling FDA records {count_results} to {next_results}")
        time.sleep(2)

        apicall = make_fda_api_call(
            skip, limit=1000, start_date="2003-01-01", end_date="2024-02-19"
        )

        if apicall is None:
            break

        results.append(apicall)
        count_results += limit
        next_results += limit
        skip += limit
        write_data(results, "fda", append=False)


def write_data(data, source, append=True):
    """
    Writes data returned by an API call to a JSON file format.

    Args:
        data (JSON): Data returned from an API call
        filename ('str'): The name of the file to write to
        append (bool): Default to true. If true, will append to the filename
        wrather than overwrite it.

    Returns:
        None. Creates or appends to the file specified.
    """

    if append:
        mode = "a"
    else:
        mode = "w"

    pth = pathlib.Path(__file__).parent / f"../../data/{source}.json"

    with open(pth, mode=mode) as f:
        f.write(json.dumps(data))


if __name__ == "__main__":
    pull_fda_api_data()
