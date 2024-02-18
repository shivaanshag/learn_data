import sys
import random
import string
import datetime
from datetime import timedelta
import pandas as pd
from random import randrange

"""
Rudimentary script to generate data conforming to the database architecture.
"""
random.seed(69420)

first_name = open("./first_names.txt", 'r')
first_names = [x.strip() for x in (first_name.readlines())]
last_name = open("./last_names.txt", 'r')
last_names = [x.strip() for x in (last_name.readlines())]
m_names = list(string.ascii_uppercase)
cities_ = pd.read_csv("uscities.csv")
cities_list = [x[:min(50, len(x))] for x in cities_["city"]]


def random_datetime(start = None):
    if not start:
        start = datetime.datetime.strptime('1/1/2012 1:30 PM', '%m/%d/%Y %I:%M %p')
    end = datetime.datetime.strptime('12/31/2022 4:50 AM', '%m/%d/%Y %I:%M %p')
    delta = end - start
    int_delta = delta.days
    seconds_delta = delta.seconds
    random_days = randrange(int_delta)
    random_seconds = randrange(seconds_delta)
    return (start + timedelta(days=random_days, seconds=random_seconds))

def random_dob(start = None):
    if not start:
        start = datetime.datetime.strptime('1/1/1980 1:30 PM', '%m/%d/%Y %I:%M %p')
    end = datetime.datetime.strptime('12/31/2022 4:50 AM', '%m/%d/%Y %I:%M %p')
    delta = end - start
    # print(end, start)
    int_delta = delta.days
    year_delta = 365 * 19
    seconds_delta = delta.seconds
    random_days = randrange(0, abs(int_delta))
    if start:
        random_days += year_delta
    random_seconds = randrange(seconds_delta)
    # print(random_days, random_seconds)
    return (start + timedelta(days=random_days, seconds=random_seconds))


def random_time(start = None):
    if not start:
        start = datetime.datetime.strptime('1:30 AM', '%I:%M %p')
    end = datetime.datetime.strptime('11:59 PM', '%I:%M %p')
    delta = end - start
    seconds_delta = delta.seconds
    random_seconds = randrange(seconds_delta)
    return (start + timedelta(seconds=random_seconds))


def employee(n, pr_list):
    pr_used_set = set()
    # if n > 899:
    #     raise Exception("out of range")
    i = 0
    eidl = set()
    emp = []
    el_sql = []
    while i < n:
        eid = 100
        while eid in eidl:
            eid = randrange(100, 999)
        eidl.add(eid)
        fname = first_names[randrange(0, len(first_names))]
        mname = m_names[randrange(0, len(m_names))]
        lname = last_names[randrange(0, len(last_names))]
        address = ''.join(random.choices(string.ascii_lowercase, k=(randrange(1,48))))
        gender = "M" if random.random()>0.5 else "F"
        
        dobdate = random_dob(None)
        edate = random_dob(dobdate).strftime('%Y-%m-%d')
        dobdate = dobdate.strftime('%Y-%m-%d')
        etype = ['Area Manager', 'Deliverer', 'Staff'][randrange(0,2)]
        pr_member_id = pr_list[0][0]
        while pr_member_id in pr_used_set:
            pr_member_id = pr_list[randrange(0, len(pr_list))][0]
        pr_used_set.add(pr_member_id)
        if len(emp) == 0:
            super_id = "NULL"
        else:
            super_id = emp[randrange(0, len(emp))][0]
        emp.append(('E'+str(eid), fname, mname, lname, address, gender, edate, dobdate, etype, pr_member_id, super_id))
        # print('E'+str(eid), fname, mname, lname, address, gender, edate, dobdate, etype, pr_member_id, super_id)  
        sqlq = create_sql_query(emp[-1], 9)
        # sqlq= '(\'E'+str(eid) + "' , '" + fname + "' , '" + mname + "' , '" + lname + "' , '" + address + "' , '" + gender + "' , '" + edate + "' , '" + dobdate + "' , '" + etype + "' , " + str(pr_member_id) + " , " + ("'E"+str(super_id) +"'" if super_id else 'NULL') + ")"
        # sqlq = sqlq.replace(",", "\',\'")
        # print(sqlq)
        sqlq =  sqlq.replace("\'NULL\'", 'NULL')
        el_sql.append(sqlq)
        # print(el_sql[-1])
        i += 1
    return eidl, emp, el_sql


def premium_member(n):
    pr_idset = set()
    pr_l = []
    pr_sql = []
    for i in range(n):
        pid = 0
        while pid in pr_idset:
            pid = randrange(0, n*50)
        pr_idset.add(pid)
        sdate = random_datetime()
        edate = random_datetime(sdate).strftime('%Y-%m-%d')
        sdate = sdate.strftime('%Y-%m-%d')
        # print("(" + str(pid) + " , '" + sdate + "' , '" + edate + "')" )
        pr_l.append((pid, sdate, edate))
        pr_sql.append(create_sql_query(pr_l[-1], 0))
        # print(pr_sql[-1])
        # pr_sql.append("(" + str(pid) + " , '" + sdate + "' , '" + edate + "')" )
    
    return pr_idset, pr_l, pr_sql


def payment(n):
    pay_idset = set()
    pay_l = []
    pay_sql = []
    for i in range(n):
        pid = 0
        while pid in pay_idset:
            pid = randrange(0, n*50)
        pay_idset.add(pid)
        pay_date = random_datetime()
        ptype = ['Electronic', 'Cash', 'Check', 'Credit Card'][randrange(0,3)]
        pay_l.append((pid, ptype, pay_date))
        pay_sql.append(create_sql_query(pay_l[-1], 0))
    
    return pay_idset, pay_l, pay_sql

def create_sql_query(l,*noinvertedidx):
    ret = "("
    for i, item in enumerate(l):
        if i != 0:
            ret+= ", "
        if i in noinvertedidx:
            ret += str(item)
        else:
            ret += "'" + str(item) + "'"
    ret += ")"
    return ret.replace("'NULL'", "NULL")

def customer(n):
    cust_idl = set()
    cust = []
    cust_sql = []
    for i in range(n):
        custid = 0
        while custid in cust_idl:
            custid = randrange(0, n*50)
        cust_idl.add(custid)
        fname = first_names[randrange(0, len(first_names))]
        mname = m_names[randrange(0, len(m_names))]
        lname = last_names[randrange(0, len(last_names))]
        cphno = randrange(1000000000, 9999999999)
        cdate = random_datetime().strftime('%Y-%m-%d')
        cust.append((custid, fname, mname, lname, cphno, cdate))
        # print(cust[-1])
        cust_sql.append(create_sql_query(list(cust[-1]), 0))
        # print(cust_sql[-1])
    return cust_idl, cust, cust_sql


def area_(n, employee):
    area_idl = set()
    area = []
    area_sql = []
    employee_ids_used = set()
    for i in range(n):
        ar = cities_list[0]
        while ar in area_idl:
            ar = cities_list[randrange(0, len(cities_list))]
        area_idl.add(ar)
        mgr_id = employee[randrange(0, len(employee))][0]
        while mgr_id in employee_ids_used:
            mgr_id = employee[randrange(0, len(employee))][0]
            if len(employee_ids_used) >= len(employee):
                mgr_id = 'NULL'
                break
        area.append((ar, mgr_id))
        area_sql.append(create_sql_query(area[-1]).replace("\'NULL\'", 'NULL'))
    return area_idl, area, area_sql



def shop_(n, employee, areas):
    shop_name = open("./company_names.txt", 'r')
    shop_names = [x.strip()[: min(49, len(x))] for x in (shop_name.readlines())]
    shop_idl = set()
    shop = []
    shop_sql = []
    # print(shop_names)
    emp_id_used = set()
    areas_used_set = set()
    for i in range(n):
        shopid = 0
        while shopid in shop_idl:
            shopid = randrange(0, n*50)
        # print(shopid)
        shop_idl.add(shopid)
        name = shop_names[randrange(0, len(shop_names))].replace("'","")
        address = ''.join(random.choices(string.ascii_lowercase, k=(randrange(1,50))))
        sphno = randrange(1000000000, 9999999999)
        area = areas[randrange(0, len(areas))][0]
        while area in areas_used_set:
            area = areas[randrange(0, len(areas))][0]

        cstartdate = random_datetime().strftime('%Y-%m-%d')

        emp_id = employee[randrange(0, len(employee))][0]
        while emp_id in emp_id_used:
            emp_id = employee[randrange[0, len(employee)]][0]

        
        shop.append((shopid, name, address, sphno, area, cstartdate, emp_id))
        # print(shop[-1])
        shop_sql.append(create_sql_query(list(shop[-1]), 0))
        
    return shop_idl, shop, shop_sql


def promotion(n, shops):
    promo_idl = set()
    promo = []
    promo_sql = []
    shops_used_set = set()
    for i in range(n):
        promoid = 0
        while promoid in promo_idl:
            promoid = randrange(0, n*50)
        # print(promoid)
        promo_idl.add(promoid)

        shop_ = shops[randrange(0, len(shops))][0]
        while shop_ in shops_used_set:
            shop_ = shops[randrange(0, len(shops))][0]
        shops_used_set.add(shop_)
        desc = ''.join(random.choices(string.ascii_lowercase, k=(randrange(1,50))))
        promo.append((promoid, desc, shop_))
        # print(promo[-1])
        # print(promo[-1])
        promo_sql.append(create_sql_query(promo[-1], 0, 2))
        # print(promo_sql[-1])
    return promo_idl, promo, promo_sql


def restaurant_type(restaurant):
    rest_type_sql = []
    for i in range(len(restaurant)):
        rest_type = ["Fast Food", "BBQ", "Buffet", "Drink", "Bistro"][randrange(0,5)]
        rest.append((restaurant[i][0], rest_type))
        # print(rest[-1])
        # print(rest[-1])
        rest_type_sql.append(create_sql_query(rest[-1], 0))
        # print(rest_sql[-1])
    return rest_type_sql


def supermarket(n, shops, restaurant_set):
    super_idl = set()
    super = []
    super_sql = []
    shops_used_set = set()
    for i in range(n):
        shop_ = shops[randrange(0, len(shops))][0]
        while shop_ in shops_used_set or shop_ in restaurant_set:
            shop_ = shops[randrange(0, len(shops))][0]
        shops_used_set.add(shop_)
        # print(shop_)
        super.append(tuple((shop_,)))
        # print(super[-1])
        super_sql.append(create_sql_query(super[-1], 0))
        # print(super_sql[-1])
    return super_idl, super, super_sql


def product(n, smarket):
    prod_idl = set()
    prod = []
    prod_sql = []
    prod_used_set = set()
    for i in range(n):
        pid = randrange(0, n*25)
        shop_ = smarket[randrange(0, len(smarket))][0]
        while (pid, shop_) in prod_used_set:
            shop_ = smarket[randrange(0, len(smarket))][0]
        prod_name = "P" + (''.join(random.choices(string.ascii_lowercase, k=(randrange(1,10)))))
        prod_desc = ''.join(random.choices(string.ascii_lowercase, k=(randrange(1,40))))
        prod_price = randrange(1, 100000) / 100
        prod_used_set.add((pid, shop_))
        # print(shop_)
        prod.append((pid, shop_, prod_name, prod_desc, prod_price))
        # print(prod[-1])
        prod_sql.append(create_sql_query(prod[-1], 0, 1, 4))
        # print(prod_sql[-1])
    return prod_idl, prod, prod_sql


def inventory(n_per, product, smarket):
    inv_idl = set()
    inv = []
    inv_sql = []

    for prod in product:
        for super in smarket:
            for i in range(n_per):
                pid = randrange(0, n_per*30*len(product) * len(smarket))
                shop_ = super[0]
                prodid = prod[0]
                while pid in inv_idl:
                    pid = randrange(0, n_per*30*len(product) * len(smarket))
                    shop_ = choose_list(smarket)[0] # smarket[randrange(0, len(smarket))][0]
                inv_idl.add(pid)

                units = randrange(0, 300)
                
                # print(shop_)
                inv.append((pid, shop_, prodid, units))
                # print(prod[-1])
                inv_sql.append(create_sql_query(inv[-1], 0, 1, 2, 3))
                # print(prod_sql[-1])
    return inv_idl, inv, inv_sql



def vehicle_(n):
    vehicle_idl = set()
    vehicle = []
    vehicle_sql = []
    vehicle_used_set = set()

    emp_used = set()
    for i in range(n):
        pid = randrange(0, n*30)
        while (pid) in vehicle_used_set:
            pid = randrange(0, n*30)
        vehicle_used_set.add(pid)

        vehicle_maker = ''.join(random.choices(string.ascii_lowercase, k=(randrange(2,9))))
        vehicle_model = ''.join(random.choices(string.ascii_lowercase, k=(randrange(2,9))))
        vehicle_color = ''.join(random.choices(string.ascii_lowercase, k=(randrange(2,9))))
        
        if randrange(0, 2):
            emp_assigned = 'NULL'
        else:
            emp_assigned = choose_list(emp)[0]
            while emp_assigned in emp_used:
                emp_assigned = choose_list(emp)[0]
            emp_used.add(emp_assigned)

        # print(shop_)
        vehicle.append((pid, vehicle_color, vehicle_maker, vehicle_model, emp_assigned))
        vehicle_sql.append(create_sql_query(vehicle[-1], 0))
        # print(vehicle_sql[-1])
    return vehicle_idl, vehicle, vehicle_sql


def choose_list(l):
    return l[randrange(0, len(l))]



def restaurant(n, shops, areas):
    rest_idl = set()
    rest = []
    rest_sql = []
    shops_used_set = set()
    area_used_set = set()
    for i in range(n):
        restid = 0
        while restid in rest_idl:
            restid = randrange(0, n*50)
        # print(restid)
        rest_idl.add(restid)

        shop_ = shops[randrange(0, len(shops))][0]
        while shop_ in shops_used_set:
            shop_ = shops[randrange(0, len(shops))][0]
        shops_used_set.add(shop_)
        
        area = areas[randrange(0, len(areas))][0]
        while area in area_used_set:
            area = areas[randrange(0, len(areas))][0]
        area_used_set.add(shop_)
        
        rest.append((shop_, area))
        # print(rest[-1])
        # print(rest[-1])
        rest_sql.append(create_sql_query(rest[-1], 0))
        # print(rest_sql[-1])
    return rest_idl, rest, rest_sql

def emp_phone(employee):
    empph = []
    empph_sql = []
    empph_set = set()
    for i, e in enumerate(employee):
        emp_id = e[0]
        for j in range(randrange(1,4)):
            mobno = randrange(1000000000, 9999999999)
            while mobno in empph_set:
                mobno = randrange(1000000000, 9999999999)
            empph_set.add(mobno)
            empph.append((emp_id, mobno))
            # print(empph[-1])
            empph_sql.append(create_sql_query(empph[-1], 1))
            # print(empph_sql[-1])
    return empph_sql
            

def silver_member(n, premium_member, customer):
    silvermem = []
    silvermem_sql = []
    silvermem_idl = set()
    cust_used = set()
    pr_mem_used = set()
    for i in range(n):
        pid = choose_list(customer)[0]
        while pid in cust_used:
            pid = choose_list(customer)[0]
        cust_used.add(pid)
        
        if randrange(0, 2):
            pr_mem = 'NULL'
        else:
            pr_mem = choose_list(premium_member)[0]
            while pr_mem in pr_mem_used:
                pr_mem = choose_list(premium_member)[0]
            pr_mem_used.add(pr_mem)
        silvermem.append((pid, pr_mem))
        silvermem_sql.append(create_sql_query(silvermem[-1], 0, 1))
    return silvermem_idl, silvermem, silvermem_sql


def member_card(sil_mem, employee):
    memcard = []
    memcard_sql = []
    for i, cust in enumerate(sil_mem):
        custid = cust[0]
        empid = choose_list(employee)[0]
        date = random_datetime().strftime('%Y-%m-%d')

        memcard.append((custid, empid, date))
        memcard_sql.append(create_sql_query(memcard[-1], 0))
    return memcard, memcard_sql


def cust_delivery_add(customer):
    custdel = []
    custdel_sql = []
    custdel_set = set()
    for cust in customer:
        custid = cust[0]
        for j in range(randrange(1,5)):
            address = ''.join(random.choices(string.ascii_lowercase, k=(randrange(1,40))))
            while address in custdel_set:
                address = ''.join(random.choices(string.ascii_lowercase, k=(randrange(1,40))))
            custdel_set.add(address)
            custdel.append((custid, address))
            # print(custdel[-1])
            custdel_sql.append(create_sql_query(custdel[-1], 0))
            # print(custdel_sql[-1])
    return custdel_sql
            

def ordinary_customer(customer, silver_member_id_set):
    ordinary_customer = []
    ordinary_customer_sql = []
    for i, cust in enumerate(customer):
        if cust[0] in silver_member_id_set:
            continue
        ordinary_customer.append((cust[0],))
        ordinary_customer_sql.append(create_sql_query(ordinary_customer[-1], 0))
    return ordinary_customer_sql


def order_(shops):
    order_idl = set()
    order = []
    order_sql = []
    order_used_set = set()
    for shop in shops:
        for i in range(randrange(1, 2000)):
            pid = randrange(0, len(shops)*300000)
            while (pid) in order_used_set:
                pid = randrange(0, len(shops)*30)
            order_used_set.add(pid)

            shopid = shop[0]

            # print(shop_)
            order.append((pid, shopid))
            order_sql.append(create_sql_query(order[-1], 0, 1))
            # print(order_sql[-1])
    return order_idl, order, order_sql


def order_content(order_):
    # order_idl = set()
    order = []
    order_sql = []
    order_used_set = set()
    for ord in order_:
        oid = ord[0]
        shopid = ord[1]
        for _ in range(randrange(1, 4)):
            content = ''.join(random.choices(string.ascii_lowercase, k=(randrange(2,18))))
            while content in order_used_set:
                content = ''.join(random.choices(string.ascii_lowercase, k=(randrange(2,18))))
            order_used_set.add(content)

            order.append((oid, shopid, content))
            # print(order[-1])
            order_sql.append(create_sql_query(order[-1], 0, 1))
        # print(order_sql[-1])
    return order_sql


def order_sub(order_):
    order_idl = set()
    order = []
    order_sql = []
    # order_used_set = set()
    for ord in order_:
        oid = ord[0]
        shopid = ord[1]
        for _ in range(randrange(1, 4)):
            subtotal = randrange(1, 100000000) / 100
            while subtotal in order_idl:
                subtotal = randrange(1, 100000000) / 100
            order_idl.add(subtotal)

            order.append((oid, shopid, subtotal))
            # print(order[-1])
            order_sql.append(create_sql_query(order[-1], 0, 1, 2))
        # print(order_sql[-1])
    return order_sql


def working_hour(shops, days):
    wk = []
    wk_sql = []
    for shop in shops:
        for day in days:
            shopid = shop[0]
            stime = random_time()
            etime = random_time(stime).strftime('%H:%M:%S')
            wk.append((shopid, day, stime.strftime('%H:%M:%S'), etime))
            wk_sql.append(create_sql_query(wk[-1], 0))
    return wk_sql


def comments(shops, customers):
    comments = []
    comments_sql = []
    for shop in shops:
        for customer in customers:
            if randrange(0,3) == 0:
                continue
            content = ''.join(random.choices(string.ascii_lowercase, k=(randrange(2,18))))
            rating = randrange(1, 6)
            comments.append((customer[0], shop[0], content, rating))
            comments_sql.append(create_sql_query(comments[-1], 0, 1, 3))
    return comments_sql


def places(orders, payments, promotion, customers):
    places = []
    places_sql = []
    for i, order in enumerate(orders):
        # cust_id = choose_list(customers)[0]
        randomno = randrange(0,6)
        if randomno == 0:
            cust_id = customers[3][0]
        elif randomno == 1:
            cust_id = customers[7][0]
        else:
            cust_id = choose_list(customers)[0]
        # cust_id = customers[3][0] if randrange(0,3) else choose_list(customers)[0]
        orderid = order[0]
        shopid = order[1]
        confirmation_id = payments[i][0]
        if randrange(0,3) != 0:
            promo = choose_list(promotion)[0]
        else:
            promo = 'NULL'
        places.append((confirmation_id, orderid, shopid, promo, cust_id))
        # print(places[-1])
        places_sql.append(create_sql_query(places[-1], 0, 1, 2, 3, 4))
    return places_sql


def delivers(orders, vehicles):
    deliver =[]
    deliver_sql = []
    for order in orders:
        orderid = order[0]
        shopid = order[1]
        vehicle = choose_list(vehicles)
        while vehicle[4] == 'NULL':
            vehicle = choose_list(vehicles)
        vehicleid = vehicle[0]
        delivererid = vehicle[4]

        deliver.append((vehicleid, delivererid, orderid, shopid))
        deliver_sql.append(create_sql_query(deliver[-1], 2, 3))
    return deliver_sql



number_employee = int(input("Enter number of employees to generate data: "))
# number_employee = 200
number_customer = number_employee*10
number_premium_member = number_employee*3
number_shop = number_employee // 2
number_promo = number_shop // 2
number_restaurant = number_shop // 3
number_products = number_restaurant * 5
number_inv_per_shop_prod = 7
number_vehicle = number_employee
number_silver_member = ( number_customer) // 4
number_ordinary_customer = number_customer - number_silver_member
days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
number_payment = number_customer*3


pr_id_set, pr, pr_sql = premium_member(number_premium_member)
emp_id_set, emp, emp_sql = employee(number_employee, pr)
cust_id_set, cust, cust_sql = customer(number_customer)
area_id_set, area, area_sql = area_(number_shop, emp)
shop_id_set, shop, shop_sql = shop_(number_shop, emp, area)
promo_id_set, promo, promo_sql = promotion(number_promo, shop)
rest_id_set, rest, rest_sql = restaurant(number_restaurant, shop, area)
rest_type_sql = restaurant_type(rest)
super_id_set,super, super_sql = supermarket(number_restaurant, shop, rest_id_set)
prod_id_set, prod, prod_sql = product(number_products, super)
inv_id_set, invt, inv_sql = inventory(number_products, prod, super)
empph_sql = emp_phone(emp)
vehicle_id_set, vehicle, vehicle_sql = vehicle_(number_vehicle)
silver_mem_id_set, silver_mem, silver_mem_sql = silver_member(number_silver_member, pr, cust)
mem_card, mem_card_sql = member_card(silver_mem, emp)
cust_del_sql = cust_delivery_add(cust)
ord_cust_sql = ordinary_customer(cust, silver_mem_id_set)
order_id_set, order, order_sql = order_(shop)
order_content_sql = order_content(order)
order_sub_sql = order_sub(order)
wk_sql = working_hour(shop, days)
comments_sql = comments(shop, cust)
paym_id_set, paym, paym_sql = payment(len(order))
places_sql = places(order, paym, promo, cust)
delivers_sql = delivers(order, vehicle)


def write_sql_to_file(ql, table_name, values_list):
    ql.write("INSERT INTO " + table_name + " VALUES\n") 
    for i, q in enumerate(values_list):
        if i == len(values_list) - 1:
            ql.write(q + ";\n")
        else:
            ql.write(q+",\n")

with open("insert.sql", 'w') as ql:
    ql.write("use db_project;\n")
    write_sql_to_file(ql, "PREMIUM_MEMBER", pr_sql)
    write_sql_to_file(ql, "EMPLOYEE", emp_sql)
    write_sql_to_file(ql, "CUSTOMER", cust_sql)
    write_sql_to_file(ql, "PAYMENT", paym_sql)
    write_sql_to_file(ql, "AREA", area_sql)
    write_sql_to_file(ql, "SHOP", shop_sql)
    write_sql_to_file(ql, "PROMOTION", promo_sql)
    write_sql_to_file(ql, "RESTAURANT", rest_sql)
    write_sql_to_file(ql, "RESTAURANT_TYPE", rest_type_sql)
    write_sql_to_file(ql, "SUPERMARKET", super_sql)
    write_sql_to_file(ql, "PRODUCT", prod_sql)
    write_sql_to_file(ql, "INVENTORY", inv_sql)
    write_sql_to_file(ql, "EMPLOYEE_PHONE", empph_sql)
    write_sql_to_file(ql, "VEHICLE", vehicle_sql)
    write_sql_to_file(ql, "SILVER_MEMBER", silver_mem_sql)
    write_sql_to_file(ql, "MEMBER_CARD", mem_card_sql)
    write_sql_to_file(ql, "CUSTOMER_DELIVERY_ADDRESS", cust_del_sql)
    write_sql_to_file(ql, "ORDINARY_CUSTOMER", ord_cust_sql)
    write_sql_to_file(ql, "ORDER_", order_sql)
    write_sql_to_file(ql, "ORDER_CONTENT", order_content_sql)
    write_sql_to_file(ql, "ORDER_SUBTOTAL", order_sub_sql)
    write_sql_to_file(ql, "WORKING_HOUR", wk_sql)
    write_sql_to_file(ql, "COMMENTS", comments_sql)
    write_sql_to_file(ql, "PLACES", places_sql)
    write_sql_to_file(ql, "DELIVERS", delivers_sql)






        

