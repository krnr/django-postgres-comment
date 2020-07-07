from django_pg_label.query import rewrite_query


def test_rewrite():
    sql = """SELECT "post_metaauthor"."id" FROM "post_metaauthor"
    WHERE ("post_metaauthor"."id" = 56901 
    AND (/*DjangoPGlabel!:some comment*/true)
    AND (/*DjangoPGlabel!:another*/true))"""

    expected = """/* some comment | another */ SELECT "post_metaauthor"."id" FROM "post_metaauthor"
    WHERE ("post_metaauthor"."id" = 56901 
   
   )"""

    assert rewrite_query(sql) == expected

