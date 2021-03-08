fetch_rates_query = """
    SELECT DATE(prices.day), AVG(prices.price),  COUNT(price) FROM prices
    INNER JOIN ports p1 ON (prices.orig_code =
        p1.code)
    INNER JOIN ports p2 ON (prices.dest_code =
        p2.code)
    WHERE 
        ((prices.orig_code = '{}') OR (p1.parent_slug = '{}'))
    AND
        ((prices.dest_code = '{}') OR  (p2.parent_slug = '{}')) 
        
    AND (DATE(prices.day) BETWEEN '{}' AND '{}')
    GROUP BY prices.day """

insert_query = """
    INSERT INTO prices (orig_code, dest_code, day, price)
    VALUES('{}', '{}', '{}', '{}')
"""