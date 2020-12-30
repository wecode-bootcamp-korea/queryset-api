# queryset-api
Project initial settings 후에 `python manage.py insert` 명령어를 실행하면 테스트에 사용될 데이터 구축이 완료된다.
```
select_related test
/books-with-all-method	books.views.BooksWithAllMethodView
/books-with-select-related	books.views.BooksWithSelectRelatedView

prefetch_related test
/stores-with-all-method	books.views.StoresWithAllMethodView
/stores-with-prefetch-related	books.views.StoresWithPrefetchRelatedView

Prefetch test
/stores-with-prefetch-none-object	books.views.StoresWithPrefetchNoneObjectView
/stores-with-prefetch-object	books.views.StoresWithPrefetchObjectView

```


## Project Structure
```
├── books
│   └── management/command
│       └── insert.py
├── queryset_api
│   └── settings.py
├── manage.py
├── decorators.py
└── requirements.txt

```
* `books`: select_related, prefetch_related, Prefetch
* `decorators` : 실행 시간을 측정할 수 있는 debugger

## Project initial settings
settings.py의 database 설정을 수정해주세요.
```python
  ex)
  DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DATABASE 명',
        'USER': 'DB접속 계정명',
        'PASSWORD': 'DB접속용 비밀번호',
        'HOST': '실제 DB 주소',
        'PORT': '포트번호',
    }
  }
```
