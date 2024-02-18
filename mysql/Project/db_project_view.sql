use db_project;

#1
create view Annual_Top_3_Customers as
SELECT cu.Customer_id, cu.First_name, cu.Last_name, count(ord.Order_id), sum(ord.Subtotal) as order_sum
FROM ORDER_SUBTOTAL as ord, PLACES as pl, CUSTOMER as cu, PAYMENT as pay
where cu.Customer_id=pl.Customer_id and ord.Order_id=pl.Order_id and pay.Confirmation_id=pl.Confirmation_id
		and datediff(CURDATE(), pay.Payment_time)<365
group by Customer_id
order by order_sum Desc
limit 3;

#2
create view Popular_Restaurant_Type as
select rest.Restaurant_type
from RESTAURANT_TYPE as rest 
where rest.Shop_id in (select top_pay_res.Shop_id from 
(select count(ord.Order_id) as order_count, ord.Shop_id
FROM RESTAURANT_TYPE as res, ORDER_ as ord, PLACES as pl, PAYMENT as pay
where ord.Shop_id = res.Shop_id	and ord.Order_id=pl.Order_id and pay.Confirmation_id=pl.Confirmation_id
		and datediff(CURDATE(), pay.Payment_time)<365
group by ord.Shop_id 
order by order_count desc limit 1) as top_pay_res);

#3
# drop view Potential_Silver_Member;
create view Potential_Silver_Member as
select cu.First_name, cu.Last_name, cu.Cust_phone_number, count(ord.Order_id) as count_order, cu.Customer_id
from PLACES as pl, CUSTOMER as cu, ORDER_ as ord, PAYMENT as pay
where pl.Customer_id=cu.Customer_id and ord.Order_id=pl.Order_id and pay.Confirmation_id=pl.Confirmation_id
		and datediff(CURDATE(), pay.Payment_time)<31
        and cu.Customer_id not in (select sm.Customer_id from SILVER_MEMBER sm) # to ensure cust is not already a silver member
group by cu.Customer_id
having count_order >10;

#4
create view Best_Area_Manager as
select count(sh.Shop_id) as shop_count, sh.Emp_id, emp.Emp_first, emp.Emp_last, emp.Emp_addr
from EMPLOYEE as emp, SHOP as sh
where emp.Emp_id = sh.Emp_id 
		and datediff(CURDATE(), sh.Contract_Start_time)<365
group by sh.Emp_id
order by shop_count desc
limit 1;

#5
create view Top_Restaurants as
WITH BB AS (select count(ord.Order_id) as order_count, res.Restaurant_type, res.Shop_id
From RESTAURANT_TYPE as res, ORDER_ as ord, PLACES as pl, PAYMENT as pay
where res.Shop_id=ord.Shop_id and pl.Order_id=ord.Order_id and pay.Confirmation_id=pl.Confirmation_id and 
	datediff(CURDATE(), pay.Payment_time)<31
group by res.Restaurant_type, res.Shop_id)
select BB.Restaurant_type, BB.Shop_id
From BB, (select max(BB.order_count) as order_count, BB.Restaurant_type From BB
group by BB.Restaurant_type) as AA
where BB.Restaurant_type = AA.Restaurant_type and BB.order_count=AA.order_count;