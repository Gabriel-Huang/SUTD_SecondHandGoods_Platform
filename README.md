# DB-Project
An online Second-hand goods trading platform for students in SUTD. A development of database-based system with Django.

## Group Members:
Huang Jiahui 10014 | Joji James Anaghan | Su Qiulin 1001415 | Wu Lingyun 1001417 | Zhang Jiaxuan 10014

## Project Proposal & Requirements
### 1. Topic:
Implementation of an online marketplace for buying and selling new and secondhand goods among SUTD. Create a web application with a database backend using Django that implements features described below. The server can run both on local machine and online.
### 2. Features to be included (equivalent to the original topic):
- 1. Registration: Login-name(unique), password. (Use Django’s auth mode and session DB module for this.)
- 2. Ordering: After registration, a user can order items that are available on the platform. (multiple copies, multiple times of ordering)
- 3. Selling: After registration, a user can post his/her item onto the platform, with a specified name, price, quantity, category, and description. (contact info??) (categories are arranged in parent-child hierarchy: we will have some big categories on the top level and some small categories under each of them)
- 4. Seller can edit product Info: (Arrival of more copies) Sellers are able to modify the quantity of the item that they are selling (School Concert ticket, 
- 5. User record: upon user demand, following info will be printed:
+ His/her account information
+ His/her full history of orders (product name, price, order quantity, order date)
+ His/her full history of feedbacks
+ List of all the feedback he/she ranked with respect to usefulness
- 6.	Feedback recordings: Users can rate or leave a short comment on a seller’ public profile -> No changes are allowed; only one feedback per user per product is allowed.
- 7.	Comment ratings: users can access a seller’s public profile and rate a comment according to this seller (numerical score 0,1 or 2)
> 8.	Goods browsing: Users can browse through items by selecting a specific category. A user can also specify that the results are to be sorted by price or average rating of the seller. We may also implement a keyword searching interface to make the search result more concrete.
> 9.	Useful feedback: Comments are displayed on a seller’s profile in the order of ratings, highest on the top and lowest at the bottom.
> 10.	Goods recommendation: We will implement Machine Learning Algorithms to build a recommendation system. 
Like most e-commerce websites, when a user orders a copy of book A, your system should give a list of other suggested books. Book B is suggested, if there exist a user X that bought both A and B. The suggested books should be sorted on decreasing sales count (i.e., most popular first); count only sales to users like X (i.e. the users who bought both A and B).
> 11.	Statistics: Every month we will provide the information of:
a.	list of n most popular sellers (in terms of items sold in this month)
b.	the list of m most popular categories

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





