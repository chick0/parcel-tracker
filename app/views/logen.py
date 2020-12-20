# -*- coding: utf-8 -*-

import json

import requests
from flask import Blueprint, Response
from bs4 import BeautifulSoup

NAME = "로젠택배"

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def check_parcel(parcel: str):
    from string import ascii_letters, punctuation, whitespace
    for s in ascii_letters + punctuation + whitespace:
        parcel = parcel.replace(s, "")

    try:
        int(parcel)
    except ValueError:
        raise ValueError("송장 번호는 숫자로만 입력해주시길 바랍니다")

    allow_length = [11]
    if len(parcel) in allow_length:
        return parcel
    else:
        raise ValueError(f"잘못된 송장 번호입니다. 송장은 {str(allow_length)}자 입니다")


def get(parcel: str):
    parcel = check_parcel(
        parcel=parcel
    )

    response = requests.get(
        url="https://www.ilogen.com/web"
    )

    cookie = response.headers['set-cookie']

    return requests.get(
        url=f"https://www.ilogen.com/web/personal/trace/{parcel}",
        cookies=dict(
            JSESSIONID=cookie.split("JSESSIONID=")[-1].split(";")[0]
        )
    )


def clean(some_str: str):
    from string import whitespace
    for i in whitespace:
        some_str = some_str.replace(i, "")
    return some_str


@bp.route("/<string:parcel>/last")
def last(parcel):
    try:
        response = get(parcel=parcel)
    except ValueError as e:
        return Response(
            response=json.dumps(
                obj=dict(
                    error=dict(
                        msg=e
                    )
                )
            ),
            mimetype="application/json",
            status=500
        )

    soup = BeautifulSoup(response.content, "html.parser")

    header = soup.find("table", {"class": "horizon pdInfo"}).find("tbody").find_all("tr")
    head = dict(
        send_by=clean(some_str=header[3].find_all("td")[1].get_text()),
        owner=clean(some_str=header[3].find_all("td")[3].get_text()),
        status=soup.find("ul", {"class": "tkStep"}).find("li", {"class": "on"}).get_text()[2:],
        item_name=clean(some_str=header[0].find_all("td")[3].get_text())
    )

    tr = soup.find("table", {"class": "data tkInfo"}).find("tbody").find_all("tr")[-1]
    td = tr.find_all("td")

    result = [
        dict(
            timestamp=td[0].get_text().replace(".", "-"),
            where=clean(some_str=td[1].get_text()),
            status=clean(some_str=td[2].get_text()),
            msg=td[3].get_text().strip()
        )
    ]

    return Response(
        response=json.dumps(
            obj=dict(
                head=head,
                track=result
            )
        ),
        mimetype="application/json",
        status=response.status_code
    )


@bp.route("/<string:parcel>")
def track_parcel(parcel: str):
    try:
        response = get(parcel=parcel)
    except ValueError as e:
        return Response(
            response=json.dumps(
                obj=dict(
                    error=dict(
                        msg=e
                    )
                )
            ),
            mimetype="application/json",
            status=500
        )

    soup = BeautifulSoup(response.content, "html.parser")

    header = soup.find("table", {"class": "horizon pdInfo"}).find("tbody").find_all("tr")
    head = dict(
        send_by=clean(some_str=header[3].find_all("td")[1].get_text()),
        owner=clean(some_str=header[3].find_all("td")[3].get_text()),
        status=soup.find("ul", {"class": "tkStep"}).find("li", {"class": "on"}).get_text()[2:],
        item_name=clean(some_str=header[0].find_all("td")[3].get_text())
    )

    result = []
    for tr in soup.find("table", {"class": "data tkInfo"}).find("tbody").find_all("tr"):
        td = tr.find_all("td")
        result.append(
            dict(
                timestamp=td[0].get_text().replace(".", "-"),
                where=clean(some_str=td[1].get_text()),
                status=clean(some_str=td[2].get_text()),
                msg=td[3].get_text().strip()
            )
        )

    return Response(
        response=json.dumps(
            obj=dict(
                head=head,
                track=result
            )
        ),
        mimetype="application/json",
        status=response.status_code
    )
