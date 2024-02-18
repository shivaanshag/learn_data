# create database db_project;
# comment out the next two lines once the creation script is finalised and the databse is already created
# TODO: add the shop id to order*, update : on update, on delete
drop database if exists db_project;
create database db_project;

use db_project;
CREATE TABLE PREMIUM_MEMBER (
    Pr_member_id NUMERIC PRIMARY KEY,
    Mp_effective_date DATE,
    Mp_expiration_date DATE
);

CREATE TABLE CUSTOMER (
    Customer_id NUMERIC PRIMARY KEY,
    First_name VARCHAR(20),
    Middle_name VARCHAR(10),
    Last_name VARCHAR(20),
    Cust_phone_number CHAR(10) DEFAULT '0000000000',
    Cust_joining_date DATE
);
    
CREATE TABLE PAYMENT (
    Confirmation_id NUMERIC PRIMARY KEY,
    P_type VARCHAR(20),
    Payment_time DATETIME
);

CREATE TABLE SHOP (
    Shop_id NUMERIC PRIMARY KEY,
    Shop_name VARCHAR(50),
    Shop_address VARCHAR(200),
    Business_phone_number CHAR(10) DEFAULT '0000000000',
    Area_name VARCHAR(50),
    Contract_start_time DATE,
    Emp_id CHAR(4)
);

CREATE TABLE EMPLOYEE (
    Emp_id CHAR(4) PRIMARY KEY,
    CONSTRAINT CHECK (REGEXP_LIKE(Emp_id, '^E[0-9]{3}') = 1),
    Emp_first VARCHAR(20),
    Emp_middle VARCHAR(10),
    Emp_last VARCHAR(20),
    Emp_addr VARCHAR(50),
    Emp_gender CHAR(1),
    Emp_designation_start_date DATE,
    Emp_date_of_birth DATE,
    Emp_type ENUM('Area Manager', 'Deliverer', 'Staff'),
    Pr_member_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Pr_member_id)
        REFERENCES PREMIUM_MEMBER (Pr_member_id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    Supervisor_id CHAR(4),
    CONSTRAINT FOREIGN KEY (Supervisor_id)
        REFERENCES EMPLOYEE (Emp_id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT CHECK (TIMESTAMPDIFF(YEAR,
        Emp_date_of_birth,
        Emp_designation_start_date) >= 18)
);

CREATE TABLE AREA (
    Area_name VARCHAR(50) PRIMARY KEY,
    Manager_id CHAR(4),
    CONSTRAINT FOREIGN KEY (Manager_id)
        REFERENCES EMPLOYEE (Emp_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

ALTER TABLE SHOP
	ADD FOREIGN KEY (Area_name) REFERENCES AREA(Area_name) ON UPDATE CASCADE ON DELETE SET NULL,
    ADD FOREIGN KEY (Emp_id) REFERENCES EMPLOYEE(Emp_id) ON UPDATE CASCADE ON DELETE SET NULL;
    
CREATE TABLE PROMOTION (
    Promo_code NUMERIC PRIMARY KEY,
    Promo_description VARCHAR(200),
    Shop_id NUMERIC NOT NULL,
    CONSTRAINT FOREIGN KEY (Shop_id)
        REFERENCES SHOP (Shop_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE RESTAURANT (
    Shop_id NUMERIC PRIMARY KEY,
    CONSTRAINT FOREIGN KEY (Shop_id)
        REFERENCES SHOP (Shop_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    R_area VARCHAR(50)
);

CREATE TABLE RESTAURANT_TYPE (
    Shop_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Shop_id)
        REFERENCES SHOP (Shop_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Restaurant_type VARCHAR(30),
    PRIMARY KEY (Shop_id , Restaurant_type)
);
    
CREATE TABLE SUPERMARKET (
    Shop_id NUMERIC PRIMARY KEY,
    CONSTRAINT FOREIGN KEY (Shop_id)
        REFERENCES SHOP (Shop_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE PRODUCT (
    Product_id NUMERIC,
    Shop_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Shop_id)
        REFERENCES SUPERMARKET (Shop_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Product_name VARCHAR(20),
    Product_description VARCHAR(200),
    Product_price NUMERIC(10 , 2 ),
    PRIMARY KEY (Product_id , Shop_id)
);
 
CREATE TABLE INVENTORY (
    Inventory_id NUMERIC,
    Shop_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Shop_id)
        REFERENCES SUPERMARKET (Shop_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Product_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Product_id)
        REFERENCES PRODUCT (Product_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Available_units NUMERIC DEFAULT 0,
    PRIMARY KEY (Inventory_id , Shop_id , Product_id)
);
    
   
CREATE TABLE EMPLOYEE_PHONE (
    Emp_id CHAR(4),
    CONSTRAINT FOREIGN KEY (Emp_id)
        REFERENCES EMPLOYEE (Emp_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Emp_phone_number CHAR(10),
    PRIMARY KEY (Emp_id , Emp_phone_number)
);
    
CREATE TABLE VEHICLE (
    Vehicle_id NUMERIC PRIMARY KEY,
    V_color VARCHAR(10),
    V_maker VARCHAR(20),
    V_model VARCHAR(20),
    Emp_id CHAR(4),
    CONSTRAINT FOREIGN KEY (Emp_id)
        REFERENCES EMPLOYEE (Emp_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE SILVER_MEMBER (
    Customer_id NUMERIC PRIMARY KEY,
    CONSTRAINT FOREIGN KEY (Customer_id)
        REFERENCES CUSTOMER (Customer_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Pr_member_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Pr_member_id)
        REFERENCES PREMIUM_MEMBER (Pr_member_id)
);

CREATE TABLE MEMBER_CARD (
    Customer_id NUMERIC PRIMARY KEY,
    CONSTRAINT FOREIGN KEY (Customer_id)
        REFERENCES SILVER_MEMBER (Customer_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Emp_id CHAR(4),
    CONSTRAINT FOREIGN KEY (Emp_id)
        REFERENCES EMPLOYEE (Emp_id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    Issuing_date DATE
);

CREATE TABLE CUSTOMER_DELIVERY_ADDRESS (
    Customer_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Customer_id)
        REFERENCES CUSTOMER (Customer_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Customer_delivery_address VARCHAR(200),
    PRIMARY KEY (Customer_id , Customer_delivery_address)
);
    
CREATE TABLE ORDINARY_CUSTOMER (
    Customer_id NUMERIC PRIMARY KEY,
    CONSTRAINT FOREIGN KEY (Customer_id)
        REFERENCES CUSTOMER (Customer_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE ORDER_ (
    Order_id NUMERIC,
    Shop_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Shop_id)
        REFERENCES SHOP (Shop_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (Order_id , Shop_id)
);

CREATE TABLE ORDER_CONTENT (
    Order_id NUMERIC,
    Shop_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Order_id , Shop_id)
        REFERENCES ORDER_ (Order_id , Shop_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Content VARCHAR(20),
    PRIMARY KEY (Order_id , Content , Shop_id)
);
    
CREATE TABLE ORDER_SUBTOTAL (
    Order_id NUMERIC,
    Shop_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Order_id , Shop_id)
        REFERENCES ORDER_ (Order_id , Shop_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Subtotal NUMERIC(10 , 2 ),
    PRIMARY KEY (Order_id , Subtotal , Shop_id)
);
    
    
CREATE TABLE DAY_ (
    Day_name CHAR(3) PRIMARY KEY
);
INSERT INTO DAY_ VALUES ('MON'), ('TUE'), ('WED'), ('THU'), ('FRI'), ('SAT'), ('SUN');

CREATE TABLE WORKING_HOUR (
    Shop_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Shop_id)
        REFERENCES SHOP (Shop_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Day_name CHAR(3),
    CONSTRAINT FOREIGN KEY (Day_name)
        REFERENCES DAY_ (Day_name)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Start_hour TIME,
    End_hour TIME,
    PRIMARY KEY (Shop_id , Day_name)
);
 
CREATE TABLE DELIVERS (
    Vehicle_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Vehicle_id)
        REFERENCES VEHICLE (Vehicle_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Emp_id CHAR(4),
    CONSTRAINT FOREIGN KEY (Emp_id)
        REFERENCES EMPLOYEE (Emp_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Order_id NUMERIC,
    Shop_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Order_id , Shop_id)
        REFERENCES ORDER_ (Order_id , Shop_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (Vehicle_id , Emp_id , Order_id , Shop_id)
);
    
CREATE TABLE COMMENTS (
    Customer_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Customer_id)
        REFERENCES CUSTOMER (Customer_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Shop_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Shop_id)
        REFERENCES SHOP (Shop_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Content VARCHAR(200),
    Rating NUMERIC(1 , 0 ),
    CHECK (Rating BETWEEN 1 AND 5),
    PRIMARY KEY (Customer_id , Shop_id)
);
    
CREATE TABLE PLACES (
    Confirmation_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Confirmation_id)
        REFERENCES PAYMENT (Confirmation_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Order_id NUMERIC,
    Shop_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Order_id , Shop_id)
        REFERENCES ORDER_ (Order_id , Shop_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    Promo_code NUMERIC,
    CONSTRAINT FOREIGN KEY (Promo_code)
        REFERENCES PROMOTION (Promo_code)
        ON UPDATE CASCADE ON DELETE SET NULL,
    Customer_id NUMERIC,
    CONSTRAINT FOREIGN KEY (Customer_id)
        REFERENCES CUSTOMER (Customer_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (Confirmation_id , Order_id , Customer_id , Shop_id)
);
    