### EndPoint
```markdown
- /
    - API에서 조회 가능한 택배 회사를 보여준다.
    - 여기서 회사 코드를 확인할 수 있다.

- /<택배 회사 코드>/<송장번호>
    - 해당 송장번호를 가지고 있는 택배를 조회한다.

- /<택배 회사 코드>/<송장번호>/last
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
            }
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
3. api 목록을 표시하는 경우
    ```json
    [
        {
            "code": "택배 회사 코드",
            "name": "회사 이름"
        }
    ]
    ```

## 도와준 사람
- cjlogistics.py
    - [KokoseiJ](https://github.com/KokoseiJ/) : csrf 토큰 관련
