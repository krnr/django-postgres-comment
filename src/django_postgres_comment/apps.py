from django.apps import AppConfig
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.backends.signals import connection_created

from django_postgres_comment.query import monkeypatch_queryset, rewrite_query


class DjangoPGCommentConfig(AppConfig):
    name = "django_postgres_comment"
    verbose_name = "PostgreSQL comments"

    def ready(self):
        add_database_instrumentation()
        monkeypatch_queryset()


def add_database_instrumentation():
    for _alias, connection in postgresql_connections():
        install_hook(connection)
    connection_created.connect(install_hook)


def install_hook(connection, **kwargs):
    if rewrite_hook not in connection.execute_wrappers:
        connection.execute_wrappers.insert(0, rewrite_hook)


def rewrite_hook(execute, sql, params, many, context):
    sql = rewrite_query(sql)
    return execute(sql, params, many, context)


def postgresql_connections():
    conn_names = [DEFAULT_DB_ALIAS] + list(set(connections) - {DEFAULT_DB_ALIAS})
    for alias in conn_names:
        connection = connections[alias]
        yield alias, connection

