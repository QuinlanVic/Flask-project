-- Sub-Query
-- 1. Write a query to display all the orders from the orders table issued by the salesman 'Paul Adam'.
SELECT * FROM salesorders WHERE salesorders.salesman_id = (SELECT salesman_id FROM salesman WHERE salesman.name = 'Paul Adam')

-- 2. Write a query to display all the orders which values are greater than the average order value for 10th October 2012.
SELECT * FROM salesorders WHERE purch_amt > (SELECT AVG(purch_amt) FROM salesorders WHERE ord_date = '2012-10-10') 

-- 3. Write a query to find all orders with order amounts which are above-average amounts for their customers. 
-- get all orders where its order amount is greater than the average for purchase amount of the customer ordering 
-- give names to tables (s1 and s2)
-- it is like a loop where each customer compares the average to their purchase amont
SELECT * FROM salesorders s1 WHERE purch_amt > (SELECT AVG(purch_amt) FROM salesorders GROUP BY customer_id HAVING customer_id = s1.customer_id) 

-- OR

-- Ragav

-- AI
-- SELECT * FROM salesorders s1 WHERE purch_amt > (SELECT AVG(s2.purch_amt) FROM salesorders s2 WHERE s1.customer_id = s2.customer_id)

-- 4. Write a query to find all orders attributed to a salesman in Mew York
SELECT * FROM salesorders WHERE salesman_id In (SELECT salesman_id FROM salesman WHERE city = 'New York')

-- 5. Write a query to find the name and numbers of all salesmen who had more than one customer
SELECT name, salesman_id FROM salesman t1 WHERE (SELECT COUNT(ord_no) FROM salesorders GROUP BY salesman_id HAVING salesman_id = t1.salesman_id) > 1
-- or
-- SELECT salesman_id, count(customer_id) as cust_count from salesorders group by salesman_id HAVING count(customer_id) > 1
SELECT * FROM salesman WHERE salesman_id In (SELECT salesman_id from salesorders group by salesman_id HAVING count(customer_id) > 1)

-- OR
-- All & Any
-- Find all the orders where purch_amt is more than gemma purch_amt
SELECT * FROM salesorders WHERE purch_amt > All ( SELECT purch_amt FROM salesorders WHERE customer_id = 3005)
SELECT * FROM salesorders WHERE purch_amt > Any ( SELECT purch_amt FROM salesorders WHERE customer_id = 3005)

-- 6. Write a query to display only those customers whose grade are, in fact, higher than every customer in New York
-- SELECT grade FROM customer WHERE city = 'New York' 

-- SELECT * FROM customer where grade > All (SELECT grade FROM customer WHERE city = 'New York')

-- 7. Write a query to find all orders with an amount smaller than any amount for a customer in London.
SELECT * FROM salesorders WHERE purch_amt < ANY(SELECT purch_amt FROM salesorders WHERE customer_id In (SELECT customer_id FROM customer WHERE city = 'London'))