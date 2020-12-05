from django_postgres_comment.query import rewrite_query


def test_rewrite():
    sql = """SELECT "post_metaauthor"."id" FROM "post_metaauthor"
    WHERE ("post_metaauthor"."id" = 56901 
    AND (/*DjangoPGComment!:some comment*/true)
    AND (/*DjangoPGComment!:another*/true))"""

    expected = """/* some comment | another */ SELECT "post_metaauthor"."id" FROM "post_metaauthor"
    WHERE ("post_metaauthor"."id" = 56901 
   
   )"""

    assert rewrite_query(sql) == expected

