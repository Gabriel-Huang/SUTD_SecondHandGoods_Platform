use platform;
-- Create Table User (
--     u_id Integer,
--     login_name Char(20) Unique,
--     password Char(20),
--     email Text(50),
--     user_pic_link Char(50),
-- 	primary key (u_id));-- 


Create Table Product ( 	#added column category
	p_id Integer,
    sellerid varchar(150),
    p_name Char(100),
    p_quantity Integer, 
    p_description Text(500),
    p_date DATETIME,
    product_pic_link Text,
    category Text,
    price float,
    primary key (p_id, sellerid),
    foreign key (sellerid) references auth_user(username));


Create Table OrderRecord (
	o_id Integer,
    productid integer Not Null,
    tradeinfo Text,
    trade_result integer,
    productseller varchar(150),
    o_quantity integer,
    buyerid varchar (150),
    o_date Date,
    primary key (o_id),
    foreign key (productid, productseller) references Product(p_id, sellerid),
    foreign key (buyerid) references auth_user(username));

    
Create Table Feedback (
	f_id Integer,
    FeedbackUser varchar (150),
    Product Integer Not Null,
    Seller varchar(150),
    f_content Text(500),
    f_score Integer check (0 <= f_score <= 10),
    f_date Date,
    unique (FeedbackUser, Product),
    primary key (f_id),
    foreign key (FeedbackUser) references auth_user(username),
    foreign key (Product, Seller) references Product (p_id, sellerid));
    

    
Create Table Rating (
	r_id Integer,
    r_score Integer check (r_score = 0 or r_score = 1 or r_score = 2),
    r_date Date,
    RatingUser varchar(150),
    FeedbackUser varchar(150),
    FeedbackProduct Integer Not Null,
    Feedback_id Integer,
    Unique (RatingUser, Feedback_id),
    primary key (r_id),
    foreign key (RatingUser) references auth_user(username),
    foreign key (Feedback_id) references Feedback (f_id),
    foreign key (FeedbackUser, FeedbackProduct) references Feedback (FeedbackUser, Product),
    Check (RaringUser <> FeedbackUser)); 
    
Create Table Search_Record(
	user varchar(150),
    content varchar(300),
    time timestamp,
    Primary Key (user, content, time),
    FOREIGN KEY (user) references auth_user(username)
);

SELECT productseller FROM (
SELECT count(o_id), productseller FROM OrderRecord
GROUP BY productseller
ORDER BY count(o_id) DESC
LIMIT 5) AS COUNT;

SELECT * FROM Product
Where p_id IN
(SELECT productid FROM (
SELECT productid, count(o_id) FROM OrderRecord
WHERE trade_result = 0
GROUP BY productid
ORDER BY count(o_id) DESC
LIMIT 5)AS COUNT);

SELECT F.f_content, score FROM(
SELECT Feedback.f_id, Feedback.f_content, AVG(Rating.r_score) AS score FROM Feedback, Rating, auth_user
WHERE Feedback.f_id = Rating.Feedback_id 
AND Feedback.FeedbackUser = 'user2'
GROUP BY Feedback.f_id
ORDER BY score DESC) AS F;