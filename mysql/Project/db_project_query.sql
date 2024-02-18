use db_project;
#1
# SELECT E1.EMP_first, E1.EMP_last FROM db_project.EMPLOYEE as E1 
# where E1.Emp_id in (SELECT EE.Supervisor_id FROM  (SELECT count(Emp_id) as deliver_count, Supervisor_id 
# 					FROM db_project.EMPLOYEE where Emp_type = 'Deliverer' 
# 					group by Supervisor_id order by deliver_count desc LIMIT 1) as EE);

#1 Alternate
select S.Emp_first,S.Emp_last, count(E.Emp_id)
from EMPLOYEE E, EMPLOYEE S
where S.Emp_id=E.Supervisor_id and E.Emp_type='Deliverer'
group by S.Emp_id
order by count(E.Emp_id) desc limit 1;


#2
select avg(count_order) from Potential_Silver_Member;

#3
# select pl.Customer_id, sh.Shop_name from ORDER_ as ord, RESTAURANT_TYPE as restyp, SHOP as sh, PLACES as pl 
# where ord.Order_id = pl.Order_id and ord.Shop_id = restyp.Shop_id and ord.Shop_id = sh.Shop_id and
# 		restyp.Restaurant_type in
# (select Ree.RESTAURANT_TYPE from (select Restaurant_type, count(Shop_id) shop_count FROM RESTAURANT_TYPE group by RESTAURANT_TYPE 
# order by shop_count desc limit 1) as Ree);

#3 Alternate
select pl.Customer_id, sh.Shop_name as Restaurant_name
from ORDER_ as ord, RESTAURANT_TYPE as restyp, SHOP as sh, PLACES as pl 
where ord.Order_id = pl.Order_id and ord.Shop_id = restyp.Shop_id and ord.Shop_id = sh.Shop_id and
		restyp.Restaurant_type in (select Restaurant_type from Popular_Restaurant_Type);

#4
SELECT cu.Customer_id, cu.First_name, cu.Last_name FROM MEMBER_CARD as memC, CUSTOMER as cu
where memC.Customer_id=cu.Customer_id and DATEDIFF(memC.Issuing_date,cu.Cust_joining_date)<31;

#5
select Em.Emp_first, Em.Emp_last from EMPLOYEE as Em where Em.Emp_id in
(select Dee.Emp_id from (SELECT De.Emp_id, count(De.Order_id) as order_count
FROM DELIVERS as De, PLACES as pl, PAYMENT as pay
where De.Order_id = pl.Order_id and De.Shop_id = pl.Shop_id and pl.Confirmation_id = pay.Confirmation_id 
	and datediff(CURDATE(), pay.Payment_time)<31
group by De.Emp_id
order by order_count desc limit 1) as Dee);

# 5 Alternate
select E.Emp_first, E.Emp_last
from EMPLOYEE E, DELIVERS D, PLACES PL, PAYMENT PAY
where D.Order_id=PL.Order_id and D.Shop_id=PL.Shop_id and PL.Confirmation_id=PAY.Confirmation_id 
	and datediff(CURDATE(), PAY.Payment_time)<31 and E.Emp_id=D.Emp_id
group by D.Emp_id
order by count(D.Order_id) desc limit 1;

#6
SELECT pr.Shop_id as restaurant_id, count(pr.Promo_code) as promo_count
FROM PROMOTION as pr, PLACES as pl, PAYMENT as pay
where pr.Promo_code = pl.Promo_code and pl.Confirmation_id = pay.Confirmation_id and datediff(CURDATE(), pay.Payment_time)<31
group by pr.Shop_id
order by promo_count desc limit 1;

#7
select distinct(plc.Customer_id) from PLACES as plc where not exists
	(SELECT * FROM RESTAURANT_TYPE as resty 
	where Restaurant_type = 'Fast Food' and resty.Shop_id not in
		(Select ord.Shop_id from PLACES as pl, ORDER_ as ord
		where pl.Order_id=ord.Order_id and pl.Customer_id=plc.Customer_id));

#8
select R.Shop_id, P.Customer_id, O.Order_id , O.total
from RESTAURANT R, PLACES P,
	(select OO.Shop_id, OO.Order_id, SUM(Subtotal) as total 
    from ORDER_ OO, ORDER_SUBTOTAL OS 
    where OO.Order_id=OS.Order_id  and OO.Shop_id=OS.Shop_id
    group by OO.Order_id, OS.Shop_id) as O
WHERE R.Shop_id=O.Shop_id and P.Order_id=O.Order_id and P.Shop_id=O.Shop_id;

#9
SELECT sh.Area_name, count(sh.Shop_id) as shop_count FROM SHOP as sh, RESTAURANT as res
Where sh.Shop_id=res.Shop_id
group by sh.Area_name
order by shop_count desc limit 1;

#10
with AA as (select count(ord.Order_id) as count_order, sh.Shop_id
	From RESTAURANT as res, ORDER_ as ord, PLACES as pl, PAYMENT as pay, SHOP sh
	where res.Shop_id=sh.Shop_id and ord.Shop_id=sh.Shop_id and ord.Order_id=pl.Order_id and pl.Confirmation_id=pay.Confirmation_id
		and datediff(CURDATE(), pay.Payment_time)<31
	group by sh.Shop_id
	order by count_order desc limit 1)
Select wo.Start_hour, wo.End_hour 
from AA, WORKING_HOUR as wo
where AA.Shop_id=wo.Shop_id;

#11
SELECT Emp_first, Emp_last 
FROM db_project.EMPLOYEE
Where Pr_member_id is not NULL;

#12
SELECT count(Product_id) as product_count, Shop_id From db_project.INVENTORY
group by Shop_id order by count(Product_id) desc limit 1;

#13
SELECT Product_id, Shop_id as supermarket, Product_name, Product_price  FROM db_project.PRODUCT order by Product_id;