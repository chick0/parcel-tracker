# -*- coding: utf-8 -*-

import json

import requests
from flask import Blueprint, Response
from bs4 import BeautifulSoup


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def check_parcel(parcel: str):
    from string import ascii_letters, punctuation, whitespace
    for s in ascii_letters + punctuation + whitespace:
        parcel = parcel.replace(s, "")

    allow_length = [12, 10]
    if len(parcel) in allow_length:
        return parcel
    else:
        raise ValueError(f"잘못된 송장 번호입니다. 송장은 {str(allow_length)}자 입니다")


def get(parcel: str):
    parcel = check_parcel(
        parcel=parcel
    )

    response = requests.get(
        url="https://www.lotteglogis.com/mobile/reservation/tracking/index"
    )

    cookie = response.headers['set-cookie']

    return requests.post(
        url="https://www.lotteglogis.com/mobile/reservation/tracking/linkView",
        data=dict(
            InvNo=parcel
        ),
        cookies=dict(
            JSESSIONID=cookie.split("JSESSIONID=")[-1].split(";")[0],
            _xm_webid_1_=cookie.split("_xm_webid_1_=")[-1].split(";")[0]
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

    head = dict(
        send_by="비공개",
        owner="비공개",
        status=soup.find("table").find_all("tr")[-1].find("td").get_text(),
        item_name="(미확인)"
    )

    tr = soup.find_all("table")[-1].find_all("tr")[1]
    td = tr.find_all("td")

    result = [
        dict(
            timestamp=td[1].get_text().replace(" ", " "),
            where=clean(td[2].get_text()),
            status=clean(td[0].get_text()),
            msg=clean(td[3].get_text())
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

    head = dict(
        send_by="비공개",
        owner="비공개",
        status=soup.find("table").find_all("tr")[-1].find("td").get_text(),
        item_name="(미확인)"
    )

    result = []
    for tr in soup.find_all("table")[-1].find_all("tr"):
        td = tr.find_all("td")
        if len(td) == 0:
            pass
        else:
            result.append(
                dict(
                    timestamp=td[1].get_text().replace(" ", " "),
                    where=clean(td[2].get_text()),
                    status=clean(td[0].get_text()),
                    msg=clean(td[3].get_text())
                )
            )

    result = list(reversed(result))

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
