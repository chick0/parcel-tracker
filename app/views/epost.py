# -*- coding: utf-8 -*-

import json

import requests
from flask import Blueprint, Response
from bs4 import BeautifulSoup

NAME = "우체국택배"

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

    allow_length = [13]
    if len(parcel) in allow_length:
        return parcel
    else:
        raise ValueError(f"잘못된 송장 번호입니다. 송장은 {str(allow_length)}자 입니다")


def get(parcel: str):
    parcel = check_parcel(
        parcel=parcel
    )

    return requests.post(
        url="https://service.epost.go.kr/trace.RetrieveDomRigiTraceList.comm",
        data=dict(
            sid1=parcel
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

    temp = soup.find("table", {"class": "table_col"}).find("tbody").find("tr")
    head = dict(
        send_by=temp.find_all("td")[0].get_text(),
        owner=temp.find_all("td")[1].get_text(),
        status=temp.find_all("td")[3].get_text(),
        item_name="(미확인)"
    )
    del temp

    t = soup.find("table", {"class": "table_col detail_off"}).find("tbody").find_all("tr")[-1]
    date = t.find_all("td")[0].get_text().replace(".", "-")
    time = t.find_all("td")[1].get_text()
    result = [
        dict(
            timestamp=f"{date} {time}",
            where=clean(t.find_all("td")[2].get_text()),
            status=clean(some_str=t.find_all("td")[-1].get_text()),
            msg=clean(some_str=t.find_all("td")[-1].get_text())
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

    temp = soup.find("table", {"class": "table_col"}).find("tbody").find("tr")
    head = dict(
        send_by=temp.find_all("td")[0].get_text(),
        owner=temp.find_all("td")[1].get_text(),
        status=temp.find_all("td")[3].get_text(),
        item_name="(비공개)"
    )
    del temp

    result = []
    for t in soup.find("table", {"class": "table_col detail_off"}).find("tbody").find_all("tr"):
        date = t.find_all("td")[0].get_text().replace(".", "-")
        time = t.find_all("td")[1].get_text()
        result.append(
            dict(
                timestamp=f"{date} {time}",
                where=clean(t.find_all("td")[2].get_text()),
                status=clean(some_str=t.find_all("td")[-1].get_text()),
                msg=clean(some_str=t.find_all("td")[-1].get_text())
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
