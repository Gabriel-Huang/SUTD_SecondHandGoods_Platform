# DB-Project
An online Second-hand goods trading platform for students in SUTD. A development of database-based system with Django.


## Group Members:
Huang Jiahui 10014 | Joji James Anaghan | Su Qiulin 1001415 | Wu Lingyun 1001417 | Zhang Jiaxuan 10014

## Project Proposal & Requirements
### 1. Topic:
Implementation of an online marketplace for buying and selling new and secondhand goods among SUTD. Create a web application with a database backend using Django that implements features described below. The server can run both on local machine and online.

### 2. Features to be included (equivalent to the original topic):
1. (5 pts) Registration: Login-name(unique), password. (Use Django’s auth mode and session DB module for this.)
2. (5 pts) Ordering: After registration, a user can order items that are available on the platform. One user can only buy one product at one time.(Enable multiple copies, multiple times of ordering)
4. (2 pts) Selling: After registration, a user can post his/her item onto the platform, with a specified name, price, quantity, category, and description.(One product has one category.)
4. (3 pts) Seller can edit product Info: (Arrival of more copies) Most second hand products only has quantity of one. Still, sellers are able to modify the quantity of the item that they are selling after uploading the product. (Eg. School Concert ticket)
3. (15 pts) User record: 
Upon user demand, the full record of a user can be seen from the user profile page: 
    1. his/her account information
    2. his/her full history of orders (product name, seller name and order status)
    3. his/her full history of feedbacks
    4. the list of all the feedbacks he/she ranked with respect to usefulness
    5. If the user is a seller:
        * his/her product list with selling status and record
        * Feedbacks he/she get from other users 

6. (2.5) Feedback recordings: Users can rate or leave a short comment on a seller’ public profile -> No changes are allowed; only one feedback per user per product is allowed.
7. (2.5) Comment ratings: users can access a seller’s public profile and rate a comment according to this seller (numerical score 1, 2 ,3, 4 or 5)
8. (20 pts)	Product browsing: Users can browse through items by selecting a specific category. A user can also specify that the results are to be sorted by price or average rating of the seller. We may also implement a keyword searching interface to make the search result more concrete.
9.	(5 pts) Useful feedback: Comments are displayed on a seller’s profile in the order of average usefulness score for feedbacks, highest on the top and lowest at the bottom.
10.	(10 pts) Product recommendation: Due to the specialness of second-hand products, most products only have one piece. Therefore, it is not approperiate to recommand products based on user's order history. The reason is, at most circumstances, the product will be out of stock after one successful order. In this case, we will not recommand products by analysing users with similar purchasing preference. Instead, we look into the search history of every user and recommand products based on the similarity score between search keywords and products. Recommendation products will be sorted on decreasing relevance. 
11.	(10 pts) Statistics: Every month we will provide the information of:
- list of n most popular sellers (in terms of items sold in this month)
- the list of m most popular categories
- the list of k most trutable users (They provided feedbacks with high usefulness score.)

## Environment Setup
Make sure you have the following installed
1. virtualenv
```
pip install virtualenv
```
2. mysql
```
sudo apt-get install mysql-server
sudo apt-get install libmysqlclient-dev
```
3. create the virtual environment
```
virtualenv $environment_name
```
activate the virtual environment by
```
source path/to/env/folder/bin/activate
```
and go to your project directory and do
```
pip install -r requirments.txt
```
## Basic Functionality
A list of basic functionalities for our platfrom

### 1. Homepage
#### a. Homepage for new user
The homepage for new users displays banners and top-sale products. New users can choose to signup for our platform by clicking the "" button in navigation bar, which links to our register page.

#### b. Homepage for registered user
The homepage will recommand products to registered user as long as he/she has search history. 

#### c. Search Function


### 2. Recommendation Product
Our recommendation system takes every user's search history. Then for each search history record, we find the top two most similar products among all products to recommend. The reason we find 2 products for each search history is that we are afraid that the data is not enough. Due to the limited space on homepage, we will only select n most frequent appeared product to recommend

### 3. Register Page

### 4. Profile Page

### 5. Product Page

### 6. Database Schema

+----------------------------+
| Tables_in_platform         |
+----------------------------+
| Feedback                   |
| OrderRecord                |
| Popular                    |
| Product                    |
| Rating                     |
| Search_Record              |
| User                       |
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
| register_profile           |
+----------------------------+

### 7. Advanced Raw SQL Query
#### a. Statistics
*	List of 5 most popular sellers (in terms of number of pending orders--the more people who wants to buy something from this seller, the more popular he/she is) 
*	List of 5 most popular items
* Average ratings for each given comment

#### b. Trigger
*   When a transaction is successfull, a trigger will check whether the product's quantity is reduced to 0, if it is, automatically decline other orders associated with this product

### 8. Demonstration on Functionalities
#### Register

After getting into the homepage, you can see how our website looks like and register as a new user by clicking on the `Register` button on the navigation bar. 

![alt text](../master/screenshots/1.png)

The page will be directed to the registration page where you can sign up as a new user by entering the user name and an appropriate password.

![alt text](../master/screenshots/2.png)

After you click `Sign Up`, you will be directed back to homepage and you can see you have login as you user name on the navigation bar `Hi, TestUser!`.

![alt text](../master/screenshots/3.png)

You can search your interested product by entering the keyword into the search bar, clicking your interested category or scroll down to the product list below to find out more.

![alt text](../master/screenshots/4.png)
![alt text](../master/screenshots/5.png)

After hitting `Enter` or clicking on the search button, you will see the products as the search results. The product name, seller name and product photo are shown on this page. Above the picture you can see the category it belongs to. You can click `Buy Now` if you are intending to buy this product.

![alt text](../master/screenshots/6.png)

You will be directed to the product information page, where you can see all the related information (name, seller, description, quantity available, category it belongs to, posting date and price) of the product in details. You can buy the product by clicking `Buy!!!`.

![alt text](../master/screenshots/7.png)

In the order page, you can leave a message to the seller to indicate your interest and/or your personal contact info and select the quantity you want. By clicking `Order!`, you can place your order.

![alt text](../master/screenshots/8.png)

You can see a status page saying `Succeed!` if the operation is successful and go back to homepage if you want by clicking `Go back to homepage`.

![alt text](../master/screenshots/9.png)

If you go back to your profile page by clicking `Hi, TestUser!`, you can see your order under the **Purchse Record** section. As the seller has yet accepted your order, you can see that your status is `Still Pending`.

![alt text](../master/screenshots/14.png)

Once the seller accepted your order, the status will change to `Succeed!` and you can leave a comment for the seller to describe your experience with the seller by clicking `comment on the seller!`.

![alt text](../master/screenshots/15.png)

![alt text](../master/screenshots/16.png)

On the seller side, he/she can check his/her order status the comment left by the buyer and the rating for the comment under the **Selling Record** section. Right now the average rating is displayed to `None` because no one has rated the comment yet.

![alt text](../master/screenshots/17.png)

If there's a third user called TestUser2 searched the same product, he/she will find out that the item has already been `SOLD OUT!` 

![alt text](../master/screenshots/18.png)

By clicking on the profile page of a seller, you can see the products that the seller is selling, available quantity for the products, other users' comments on the seller and the average rating for the comments.

![alt text](../master/screenshots/19.png)

You can rate the comments in the scale of 1-5 starts to indicate the usefulness of the comment:

![alt text](../master/screenshots/20.png)

If someone rates the comments, the seller can see the changes on his/her average rating.

![alt text](../master/screenshots/21.png)

If you want to become a seller in the system, you can click the `Sell an item!` on the navigation bar. You will be directed to a new page to fill out the information for the product you want to sell, including `Product name`, `Description`, `Price`, `Quantity`, `Category` and `Product photo`.

![alt text](../master/screenshots/11.png)

If other user click on your Profile page, they can see the product you want to sell. By clicking `More`, they can see the product page with all the details.

![alt text](../master/screenshots/22.png)
