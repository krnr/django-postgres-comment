## preface

мы хотим иметь возможность добавить "метку" в начале каждого запроса,
чтобы потом иметь возможность отслеживать запрос в `pg_stat_activity` и
Elastic APM.

Существующая архитектура Django предполагает решения в стиле "[давайте](https://github.com/shezadkhan137/django-sql-commenter/blob/master/django_sql_commenter/db/backends/shared/commenter_cursor.py) [патчить](https://github.com/adw0rd/django-sql-stacktrace/blob/master/sqlstacktrace/stacktracecursor.py) [курсор](https://groups.google.com/d/msg/django-developers/14ixsfu4VAw/XcWlpxLtm1EJ)":

но этого не позволяет устанавливать комменты для каждого запроса:

```sql
/* select all from post table */
SELECT * from post_post

/* select all from incident table */
SELECT * from incident_incident
```

Чтобы у кваерисета появился подобный метод:

```python
def set_label(self, text: str):
    ...
```

не достаточно просто присвоить существующему классу миксин, поскольку хранить эту информацию (а тем более вставить перед директивой `SELECT`) попросту негде.

как вариант можно сделать свой класс бэкенда, который использует свой класс компилятора, который смотрит в `query.__comment`, который содержит собственно коммент из метода. в обсуждении с core-developer адамом джонсоном (автор https://github.com/django/django/pull/4495), это было признано наилучшим способом, но также самым трудоемким. поэтому за пример была взята его библиотека `django_mysql`, где комментарий хранится в экстре, а потом [берется оттуда](https://github.com/adamchainz/django-mysql/blob/master/src/django_mysql/apps.py#L51).

для осуществления манипуляций с текстом SQL запроса существует context-manager [`with connection.execute_wrapper:`](https://docs.djangoproject.com/en/3.0/topics/db/instrumentation/#connection-execute-wrapper). в нем регулярными выражениями из экстры будет убран текст комментария и - если больше в ней ничего нет - условие исполнения (`WHERE (true)`), без которого нельзя создать ноду с select-ом.

## использование

при старте апп-а происходит конфигурация: идет monkeypatch класса `QuerySet` в `django`, который дает нам
искомый метод:

```python
Notification.objects.annotate(user_from_data=KeyTransform("user_id", "data")).set_label("booy")[:10]
```
```sql
/*  booy  */ SELECT "webhooks_notification"."id",
       "webhooks_notification"."client_id",
       "webhooks_notification"."created",
       "webhooks_notification"."read",
       "webhooks_notification"."sent_to_user",
       "webhooks_notification"."delivered",
       "webhooks_notification"."data",
       "webhooks_notification"."user_id",
       ("webhooks_notification"."data" -> 'user_id') AS "user_from_data"
  FROM "webhooks_notification"
 LIMIT 10
```

плюсы такого подхода:

- простота в реализации и поддержке
- не нужны дополнительные опции в настройках (если тебе не нужны лейблы, ты просто не заводишь эту библиотеку)

*"а что если я хочу, чтобы стоп-слово искалось не во всех запросах?"* ну тогда добро пожаловать down the "my-own-backend-with-a-compiler" route.

## breadcrumbs

при многократном использовании кваерисета в итоговом запросе будут все комментарии:

```python
qs = Ticket.objects.all().set_label("all tickets")
qs = qs.filter(price__gt=100).set_label("greater than a hundred")
```
```sql
(0.012) /*  all tickets  |  greater than a hundred  */ SELECT "main_app_ticket"."id",
  "main_app_ticket"."performance_id",
  "main_app_ticket"."price" 
FROM "main_app_ticket" WHERE ("main_app_ticket"."price" > 100)  LIMIT 21; args=(100,)
```

при этом, если сделать `print(qs.query)`, то запрос будет выведен как есть - со стоп-словом, без манипуляций c SQL.
