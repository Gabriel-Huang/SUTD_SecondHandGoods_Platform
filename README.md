# DB-Project
An online 2nd hand goods trading platform for students in SUTD

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





