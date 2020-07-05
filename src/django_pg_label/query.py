import inspect
import re

from django.db.models import QuerySet

STOP_WORD = "DjangoPGlabel!:"
ALWAYS = "true"
query_rewrite_re = re.compile(r"/\*" + STOP_WORD + r"(.*?)\*/")
where_re = re.compile(r"(WHERE \(true\)) | (AND \(true\))")


def rewrite_query(sql: str):
    """Combine SQL with added comment."""
    matches = query_rewrite_re.findall(sql)
    if matches:
        comment = matches[0]
        sql = query_rewrite_re.sub("", sql)
        sql = where_re.sub("", sql)
        sql = f"/* {comment} */ {sql}"
    return sql


def monkeypatch_queryset():
    """Patch QuerySet with the set_label method"""
    @monkey(QuerySet)
    def set_label(self, txt: str):
        return self.extra(where=[f"/*{STOP_WORD} {txt} */{ALWAYS}"])


def monkey(cls, name=None):
    """Monkey patches class or module by adding decorated function to it.

    Anything overwritten could be accessed via .original attribute of decorated object.
    """
    err = "Attempting to monkey patch non-class and non-module"
    assert inspect.isclass(cls) or inspect.ismodule(cls), err

    def cut_prefix(s, prefix):
        """Cuts prefix from given string if it's present."""
        return s[len(prefix) :] if s.startswith(prefix) else s

    def decorator(value):
        func = getattr(value, "fget", value)  # Support properties
        func_name = name or cut_prefix(func.__name__, "%s__" % cls.__name__)

        func.__name__ = func_name
        func.original = getattr(cls, func_name, None)

        setattr(cls, func_name, value)
        return value

    return decorator
