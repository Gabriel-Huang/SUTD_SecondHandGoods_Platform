-- Popular seller

SELECT productseller FROM (
SELECT count(o_id), productseller FROM OrderRecord
GROUP BY productseller
ORDER BY count(o_id) DESC
LIMIT 5) AS COUNT;

-- Popular items

SELECT * FROM Product
Where p_id IN
(SELECT productid FROM (
SELECT productid, count(o_id) FROM OrderRecord
WHERE trade_result = 0
GROUP BY productid
ORDER BY count(o_id) DESC
LIMIT 5)AS COUNT);

-- Average rating for given comment

SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));

SELECT p_name, F.f_date, F.f_content, score FROM(
SELECT p_name, Feedback.f_id, Feedback.f_date, Feedback.f_content, AVG(Rating.r_score) AS score FROM Feedback, auth_user, Product, Rating
WHERE Feedback.f_id = Rating.Feedback_id 
AND Feedback.FeedbackUser = 'gil1'
GROUP BY Feedback.f_id
ORDER BY score DESC) AS F;


