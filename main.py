import json

import requests
from bs4 import BeautifulSoup


def processJob(job):
    url = f"https://careers.airbnb.com/positions/{job['id']}"
    response = requests.get(url)
    # print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())
    payRange = soup.find("div", {"class": "pay-range"})
    if payRange:
        payRange = payRange.text.strip()
        job["minSalary"] = float(payRange.split("—")[0][1:].replace(",", ""))
        job["maxSalary"] = float(payRange.split("—")[1][1:].replace(",", "").split(" ")[0])
        job["currency"] = payRange.split(" ")[-1]
    else:
        job["minSalary"] = None
        job["maxSalary"] = None
        job["currency"] = None
    print(job)


def main():
    url = "https://careers.airbnb.com/wp-admin/admin-ajax.php"
    params = {
        "action": "fetch_greenhouse_jobs",
        "which-board": "airbnb",
        "strip-empty": "true"
    }
    response = requests.get(url, params=params)
    parsedResponse = response.json()
    with open("airbnb.json", "w") as f:
        json.dump(parsedResponse, f, indent=4)
    departments = {}
    for department in parsedResponse['departments']:
        departments[department['id']] = department['name']
    for job in parsedResponse['jobs']:
        data = {
            "id": job['id'],
            "title": job['title'],
            "location": job['location'],
            "locations": ", ".join([location['locationName'] for location in job['locations']]),
            "department": departments[job['deptId']],
        }
        print(data)
        processJob(data)


if __name__ == '__main__':
    main()
