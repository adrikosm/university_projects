-- 1)
EXPLAIN PLAN SET STATEMENT_ID = 'ex4.1' FOR
SELECT
  /*+
  NO_INDEX(C CUSTOMERS_IDX)
  NO_INDEX(P PRODUCTS_CATEGORYNAME_IDX)
  */ ORDER_ID, PRICE - COST, DAYS_TO_PROCESS
FROM PRODUCTS P
  JOIN ORDERS O ON O.PRODUCT_ID = P.PRODUCT_ID
  JOIN CUSTOMERS C ON O.CUSTOMER_ID = C.CUSTOMER_ID
WHERE P.CATEGORYNAME = 'Accessories'
    AND O.CHANNEL = 'Internet'
    AND C.GENDER = 'Male'
    AND C.INCOME_LEVEL = 'high'
    AND O.DAYS_TO_PROCESS > 100;

SELECT COST, CPU_COST, IO_COST FROM PLAN_TABLE
WHERE STATEMENT_ID = 'ex4.1' AND ID = 0;

SELECT * FROM TABLE(
    DBMS_XPLAN.DISPLAY(STATEMENT_ID => 'ex4.1')
);
/*
---------------------------------------------------------------------------------
| Id  | Operation           | Name      | Rows  | Bytes | Cost (%CPU)| Time     |
---------------------------------------------------------------------------------
|   0 | SELECT STATEMENT    |           |  3536 |   258K|   868   (1)| 00:00:01 |
|*  1 |  HASH JOIN          |           |  3536 |   258K|   868   (1)| 00:00:01 |
|*  2 |   TABLE ACCESS FULL | CUSTOMERS |  4464 | 75888 |    79   (0)| 00:00:01 |
|*  3 |   HASH JOIN         |           |  4834 |   273K|   789   (1)| 00:00:01 |
|*  4 |    TABLE ACCESS FULL| PRODUCTS  |    10 |   180 |     3   (0)| 00:00:01 |
|*  5 |    TABLE ACCESS FULL| ORDERS    | 34803 |  1359K|   786   (1)| 00:00:01 |
---------------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------

1 - access("O"."CUSTOMER_ID"="C"."CUSTOMER_ID")
2 - filter("C"."INCOME_LEVEL"='high' AND "C"."GENDER"='Male')
3 - access("O"."PRODUCT_ID"="P"."PRODUCT_ID")
4 - filter("P"."CATEGORYNAME"='Accessories')
5 - filter("O"."CHANNEL"='Internet' AND "O"."DAYS_TO_PROCESS">100)
*/

-- 2)
EXPLAIN PLAN SET STATEMENT_ID = 'ex4.2' FOR
SELECT ORDER_ID, PRICE - COST, DAYS_TO_PROCESS
FROM PRODUCTS P
  JOIN ORDERS O ON O.PRODUCT_ID = P.PRODUCT_ID
  JOIN CUSTOMERS C ON O.CUSTOMER_ID = C.CUSTOMER_ID
WHERE P.CATEGORYNAME = 'Accessories'
    AND O.CHANNEL = 'Internet'
    AND C.GENDER = 'Male'
    AND C.INCOME_LEVEL = 'high'
    AND O.DAYS_TO_PROCESS > 100;

SELECT COST, CPU_COST, IO_COST FROM PLAN_TABLE
WHERE STATEMENT_ID = 'ex4.2' AND ID = 0;

SELECT * FROM TABLE(
    DBMS_XPLAN.DISPLAY(STATEMENT_ID => 'ex4.2')
);
/*
-------------------------------------------------------------------------------------------------------------------
| Id  | Operation                             | Name                      | Rows  | Bytes | Cost (%CPU)| Time     |
-------------------------------------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT                      |                           |  3536 |   258K|   788   (1)| 00:00:01 |
|   1 |  NESTED LOOPS                         |                           |  3536 |   258K|   788   (1)| 00:00:01 |
|*  2 |   HASH JOIN                           |                           |  4834 |   273K|   788   (1)| 00:00:01 |
|   3 |    TABLE ACCESS BY INDEX ROWID BATCHED| PRODUCTS                  |    10 |   180 |     2   (0)| 00:00:01 |
|*  4 |     INDEX RANGE SCAN                  | PRODUCTS_CATEGORYNAME_IDX |    10 |       |     1   (0)| 00:00:01 |
|*  5 |    TABLE ACCESS FULL                  | ORDERS                    | 34803 |  1359K|   786   (1)| 00:00:01 |
|*  6 |   INDEX UNIQUE SCAN                   | CUSTOMERS_IDX             |     1 |    17 |     0   (0)| 00:00:01 |
-------------------------------------------------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------

   2 - access("O"."PRODUCT_ID"="P"."PRODUCT_ID")
   4 - access("P"."CATEGORYNAME"='Accessories')
   5 - filter("O"."CHANNEL"='Internet' AND "O"."DAYS_TO_PROCESS">100)
   6 - access("O"."CUSTOMER_ID"="C"."CUSTOMER_ID" AND "C"."GENDER"='Male' AND "C"."INCOME_LEVEL"='high')
*/

