-- 1)
BEGIN
  drop_index('PRODUCTS_CATEGORYNAME_IDX');
  drop_index('CUSTOMERS_IDX');
END;
/

EXPLAIN PLAN SET STATEMENT_ID = 'ex3.1' FOR
SELECT ORDER_ID, PRICE - COST, DAYS_TO_PROCESS
FROM PRODUCTS P
  JOIN ORDERS O ON O.PRODUCT_ID = P.PRODUCT_ID
  JOIN CUSTOMERS C ON O.CUSTOMER_ID = C.CUSTOMER_ID
WHERE P.CATEGORYNAME = 'Accessories'
    AND O.CHANNEL = 'Internet'
    AND C.GENDER = 'Male'
    AND C.INCOME_LEVEL = 'high'
    AND O.DAYS_TO_PROCESS = 0;

SELECT COST, CPU_COST, IO_COST FROM PLAN_TABLE
WHERE STATEMENT_ID = 'ex3.1' AND ID = 0;
SELECT * FROM TABLE(
    DBMS_XPLAN.DISPLAY(STATEMENT_ID => 'ex3.1')
);
/*
---------------------------------------------------------------------------------
| Id  | Operation           | Name      | Rows  | Bytes | Cost (%CPU)| Time     |
---------------------------------------------------------------------------------
|   0 | SELECT STATEMENT    |           |   883 | 66225 |   868   (1)| 00:00:01 |
|*  1 |  HASH JOIN          |           |   883 | 66225 |   868   (1)| 00:00:01 |
|*  2 |   HASH JOIN         |           |   883 | 51214 |   789   (1)| 00:00:01 |
|*  3 |    TABLE ACCESS FULL| PRODUCTS  |    10 |   180 |     3   (0)| 00:00:01 |
|*  4 |    TABLE ACCESS FULL| ORDERS    |  6357 |   248K|   786   (1)| 00:00:01 |
|*  5 |   TABLE ACCESS FULL | CUSTOMERS |  4464 | 75888 |    79   (0)| 00:00:01 |
---------------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------

   1 - access("O"."CUSTOMER_ID"="C"."CUSTOMER_ID")
   2 - access("O"."PRODUCT_ID"="P"."PRODUCT_ID")
   3 - filter("P"."CATEGORYNAME"='Accessories')
   4 - filter("O"."DAYS_TO_PROCESS"=0 AND "O"."CHANNEL"='Internet')
   5 - filter("C"."INCOME_LEVEL"='high' AND "C"."GENDER"='Male')
 */

-- 2)
SELECT CARDINALITY FROM PLAN_TABLE
WHERE STATEMENT_ID = 'ex3.1' AND ID = 0;
SELECT COUNT(*)
FROM PRODUCTS P
  JOIN ORDERS O ON O.PRODUCT_ID = P.PRODUCT_ID
  JOIN CUSTOMERS C ON O.CUSTOMER_ID = C.CUSTOMER_ID
WHERE P.CATEGORYNAME = 'Accessories'
    AND O.CHANNEL = 'Internet'
    AND C.GENDER = 'Male'
    AND C.INCOME_LEVEL = 'high'
    AND O.DAYS_TO_PROCESS = 0;

-- 3)
CREATE INDEX PRODUCTS_CATEGORYNAME_IDX
  ON PRODUCTS (CATEGORYNAME);
CREATE UNIQUE INDEX CUSTOMERS_IDX
  ON CUSTOMERS (CUSTOMER_ID, GENDER, INCOME_LEVEL);

EXPLAIN PLAN SET STATEMENT_ID = 'ex3.3' FOR
SELECT ORDER_ID, PRICE - COST, DAYS_TO_PROCESS
FROM PRODUCTS P
  JOIN ORDERS O ON O.PRODUCT_ID = P.PRODUCT_ID
  JOIN CUSTOMERS C ON O.CUSTOMER_ID = C.CUSTOMER_ID
WHERE P.CATEGORYNAME = 'Accessories'
    AND O.CHANNEL = 'Internet'
    AND C.GENDER = 'Male'
    AND C.INCOME_LEVEL = 'high'
    AND O.DAYS_TO_PROCESS = 0;

SELECT COST FROM PLAN_TABLE
WHERE STATEMENT_ID = '3.3' AND ID = 0;

SELECT * FROM TABLE(
    DBMS_XPLAN.DISPLAY(STATEMENT_ID => 'ex3.3')
);
/*
-------------------------------------------------------------------------------------------------------------------
| Id  | Operation                             | Name                      | Rows  | Bytes | Cost (%CPU)| Time     |
-------------------------------------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT                      |                           |   883 | 66225 |   788   (1)| 00:00:01 |
|   1 |  NESTED LOOPS                         |                           |   883 | 66225 |   788   (1)| 00:00:01 |
|*  2 |   HASH JOIN                           |                           |   883 | 51214 |   788   (1)| 00:00:01 |
|   3 |    TABLE ACCESS BY INDEX ROWID BATCHED| PRODUCTS                  |    10 |   180 |     2   (0)| 00:00:01 |
|*  4 |     INDEX RANGE SCAN                  | PRODUCTS_CATEGORYNAME_IDX |    10 |       |     1   (0)| 00:00:01 |
|*  5 |    TABLE ACCESS FULL                  | ORDERS                    |  6357 |   248K|   786   (1)| 00:00:01 |
|*  6 |   INDEX UNIQUE SCAN                   | CUSTOMERS_IDX             |     1 |    17 |     0   (0)| 00:00:01 |
-------------------------------------------------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------

   2 - access("O"."PRODUCT_ID"="P"."PRODUCT_ID")
   4 - access("P"."CATEGORYNAME"='Accessories')
   5 - filter("O"."DAYS_TO_PROCESS"=0 AND "O"."CHANNEL"='Internet')
   6 - access("O"."CUSTOMER_ID"="C"."CUSTOMER_ID" AND "C"."GENDER"='Male' AND "C"."INCOME_LEVEL"='high')

cpu_cost = 188418202, io_cost = 783
 */

