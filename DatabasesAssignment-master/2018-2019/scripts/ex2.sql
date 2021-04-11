-- i) Find the biggest delay for each order
SELECT ORDER_ID, MAX(DAYS_TO_PROCESS) AS BIGGEST_DELAY
FROM ORDERS WHERE DAYS_TO_PROCESS > 10 GROUP BY ORDER_ID;

-- ii) Find the profit/deficit of each product
SELECT O.ORDER_ID, P.PRODUCT_ID,
  TRUNC(O.PRICE - O.COST - 0.0001 * P.LIST_PRICE, 2) AS PROFIT
FROM PRODUCTS P JOIN ORDERS O ON P.PRODUCT_ID = O.PRODUCT_ID;

-- iii) Create PROFIT & DEFICIT tables
CALL drop_table('PROFIT');
CREATE TABLE PROFIT (
  ORDER_ID NUMBER(*),
  CUSTOMER_ID NUMBER(*),
  CHANNEL VARCHAR2(20),
  AMOUNT NUMBER(*)
);

CALL drop_table('DEFICIT');
CREATE TABLE DEFICIT AS SELECT * FROM PROFIT;

DECLARE
  profit_tuple PROFIT%ROWTYPE;
  CURSOR profit_cursor IS
    SELECT O.ORDER_ID, O.CUSTOMER_ID, O.CHANNEL,
      TRUNC(SUM(O.PRICE - O.COST - 0.0001 * P.LIST_PRICE), 2) AS AMOUNT
    FROM PRODUCTS P JOIN ORDERS O ON P.PRODUCT_ID = O.PRODUCT_ID
    GROUP BY P.PRODUCT_ID, O.ORDER_ID, O.CUSTOMER_ID, O.CHANNEL;
BEGIN
  FOR profit_tuple IN profit_cursor LOOP
    IF profit_tuple.AMOUNT > 0 THEN
      INSERT INTO PROFIT VALUES (
        profit_tuple.ORDER_ID,
        profit_tuple.CUSTOMER_ID,
        profit_tuple.CHANNEL,
        profit_tuple.AMOUNT
      );
    ELSE
      INSERT INTO DEFICIT VALUES (
        profit_tuple.ORDER_ID,
        profit_tuple.CUSTOMER_ID,
        profit_tuple.CHANNEL,
        ABS(profit_tuple.AMOUNT)
      );
    END IF;
  END LOOP;
  COMMIT;
END;
/

-- iv) Find the total profit/deficit per gender
SELECT
  C.GENDER AS CUSTOMER_GENDER,
  SUM(P.AMOUNT) AS TOTAL_PROFIT,
  SUM(D.AMOUNT) AS TOTAL_DEFICIT
FROM PROFIT P
  JOIN DEFICIT D ON P.CUSTOMER_ID = D.CUSTOMER_ID
  JOIN CUSTOMERS C ON P.CUSTOMER_ID = C.CUSTOMER_ID
GROUP BY C.GENDER;
/*
Male,1288541.18,58107.68
Female,856590.6,36187.7
*/

-- v) Find the total profit/deficit per channel
SELECT
  P.CHANNEL AS ORDER_CHANNEL,
  SUM(P.AMOUNT) AS TOTAL_PROFIT,
  SUM(D.AMOUNT) AS TOTAL_DEFICIT
FROM PROFIT P
  JOIN DEFICIT D ON P.CUSTOMER_ID = D.CUSTOMER_ID
GROUP BY P.CHANNEL;
/*
Direct Sales,1026668.39,41957.73
Partners,612302.71,29623.31
Internet,506160.68,22714.34
*/

