# -*- coding: utf-8 -*-

class App:                 # 앱 관련
    # 앱 이름
    name = "parcel-tracker"


class Server:              # 서버 관련
    # 포트 번호
    port = 8282


class Log:                 # 로그 관련
    # 시작시간
    from datetime import datetime
    now = datetime.today()

    # 파일명
    from os import path, mkdir

    if not path.isdir(path.join("log")):
        mkdir("log")

    name = f"{now.strftime('%Y-%m-%d %Hh %Mm %Ss')}.log"
    file = path.join("log", name)
