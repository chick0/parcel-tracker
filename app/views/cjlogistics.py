# -*- coding: utf-8 -*-

import re
import json

import requests
from flask import Blueprint, Response

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
        url="https://www.cjlogistics.com/ko/tool/parcel/tracking"
    )

    cookie = response.headers['set-cookie']
    csrf_value = re.findall(
        pattern=b"var GLOBAL_CSRF_VALUE = \"(.*?)\";",
        string=response.content
    )[0].decode(encoding="utf-8")

    return requests.post(
        url="https://www.cjlogistics.com/ko/tool/parcel/tracking-detail",
        data=dict(
            _csrf=csrf_value,
            paramInvcNo=parcel
        ),
        cookies=dict(
            SCOUTER=cookie.split("SCOUTER=")[-1].split(";")[0],
            cjlogisticsFrontLangCookie=cookie.split("cjlogisticsFrontLangCookie=")[-1].split(";")[0],
            JSESSIONID=cookie.split("JSESSIONID=")[-1].split(";")[0]
        )
    )


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

    head = response.json()['parcelResultMap']['resultList'][0]
    track = response.json()['parcelDetailResultMap']['resultList'][-1]

    head = dict(
        send_by=head['sendrNm'],
        owner=head['rcvrNm'],
        status=track['scanNm'],
        item_name=head['itemNm']
    )

    result = [
        dict(
            timestamp=track['dTime'].split(".")[0],
            where=track['regBranNm'],
            status=track['scanNm'],
            msg=track['crgNm']
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

    head = response.json()['parcelResultMap']['resultList'][0]
    track = response.json()['parcelDetailResultMap']['resultList']

    head = dict(
        send_by=head['sendrNm'],
        owner=head['rcvrNm'],
        status=track[-1]['scanNm'],
        item_name=head['itemNm']
    )

    result = []
    for obj in track:
        result.append(
            dict(
                timestamp=obj['dTime'].split(".")[0],
                where=obj['regBranNm'],
                status=obj['scanNm'],
                msg=obj['crgNm']
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
