# -*- coding: utf-8 -*-

class App:
    # API 서버가 동작할 포트를 지정합니다.
    # 기본 값은 '8082' 이며 nginx를 통한 리버스 프록시(reverse proxy)를 권장함
    port = 8282


class Log:
    # 웹 서버 로그를 남길 파일명을 정한다.
    project = "parcel-tracker"
    file = f"{project}.log"
