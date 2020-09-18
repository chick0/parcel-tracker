# parcel tracker
- Python 택배 api

## 도움말
### 설치 방법
```markdown
1. 'requirements.txt'에 설치된 패키지를 설치한다.
    - 'pip install -r requirements.txt'
2. 해당 api서버가 사용할 포트가 이미 사용중인지 확인한다.
    - 기본 값: 8282
    - 'option.py' 에서 변경이 가능함
3. 'production.py'를 실행시키면 끝
    - Linux: python3 production.py [or] python production.py
    - Windows: production.py [or] python production.py
```



## API
### EndPoint
```markdown
- /<택배회사>/<송장번호>
    - 해당 송장번호를 가지고 있는 택배를 조회한다.

- /<택배회사>/<송장번호>/last
    - 해당 송장번호를 가지고 있는 택배의 마지막 상태를 조회한다.
```

### Response
1. 정상적인 경우
    ```json
    {
        "head": {
            "send_by": "보내는 사람 (또는 '비공개')",
            "owner": "받는 사람 (또는 '비공개')",
            "status": "상태 [배송중/배송완료/ ... ]",
            "item_name": "상품명 (또는 '미확인')"
        },
        "track": [
            {
                "timestamp": "YYYY-MM-DD HH:MM",
                "where": "택배의 현 위치",
                "status": "상태 [배송중/배송완료/ ... ]",
                "msg": "상태 설명 (택배 회사에 따라 공백 일수 도 있음)"
            } // last 로 요청한 것이 아니면 여러개가 반환됨
        ]
    }
    ```
2. 오류가 발생한 경우
    ```json
    {
        "error": {
            "msg": "오류 메시지"
        }
    }
    ```


## 기여자
- cjlogistics.py
    - [KokoseiJ](https://github.com/KokoseiJ/) : csrf 토큰 관련
