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
* User (Auth)

* Product

* OrderRecord

* Search_Record

* Feedback

* Rating


### 7. Raw SQL Query
#### a. Statistics
*	List of 5 most popular sellers (in terms of number of pending orders--the more people who wants to buy something from this seller, the more popular he/she is) 
*	List of 5 most popular items
* Average ratings for each given comment

### 8. Demonstration
#### Register

After getting into the homepage, you can see how our website looks like and register as a new user by clicking on the `Register` button on the navigation bar. 

![alt text](../master/1.png)

The page will be directed to the registration page where you can sign up as a new user by entering the user name and an appropriate password.

![alt text](../master/2.png)

After you click `Sign Up`, you will be directed back to homepage and you can see you have login as you user name on the navigation bar (`Hi TestUser!`).

![alt text](../master/3.png)

