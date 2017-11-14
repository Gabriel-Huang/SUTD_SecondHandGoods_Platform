use platform;
Create Table User (
    u_id Integer,
    login_name Char(20) Unique,
    password Char(20),
    email Text(50),
    user_pic_link Char(50),
	primary key (u_id));
    
Create Table Product (
	p_id Integer,
    sellerid Integer Not Null,
    sellername Char(20),
    p_name Char(100),
    p_quantity Integer, 
    p_description Text(500),
    p_date Date,  # auto assign current date
    product_pic_link Text(100),
    primary key (p_id, sellerid),
    foreign key (sellerid) references User(u_id));

Create Table Category (
	c_id Integer primary key,
    c_name Char(20));

Create Table HasCategory (
	p_id Integer,
    c_id Integer,
    primary key (p_id, c_id),
    foreign key (p_id) references Product(p_id),
    foreign key (c_id) references Category(c_id));

Create Table OrderRecord (
	o_id Integer,
    productid integer Not Null,
    productseller integer Not Null,
    o_quantity integer,
    buyerid integer Not Null,
    o_date Date,
    primary key (o_id),
    foreign key (productid, productseller) references Product(p_id, sellerid),
    foreign key (buyerid) references User(u_id));
    
    
Create Table Feedback (
	f_id Integer,
    FeedbackUser Integer Not Null,
    Product Integer Not Null,
    Seller Integer Not Null,
    f_content Text(500),
    f_score Integer check (0 <= score <= 10),
    f_date Date,
    unique (FeedbackUser, Product),
    primary key (f_id),
    foreign key (FeedbackUser) references User(u_id),
    foreign key (Product, Seller) references Product (p_id, sellerid));
    

    
Create Table Rating (
	r_id Integer,
    r_score Integer check (r_score = 0 or r_score = 1 or r_score = 2),
    r_date Date,
    RatingUser Integer Not Null,
    FeedbackUser Integer Not Null,
    FeedbackProduct Integer Not Null,
    Unique (RatingUser, Feedback),
    primary key (r_id),
    foreign key (RatingUser) references User(u_id),
    foreign key (FeedbackUser, FeedbackProduct) references Feedback (FeedbackUser, Product),
    Check (RaringUser != FeedbackUser));
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    