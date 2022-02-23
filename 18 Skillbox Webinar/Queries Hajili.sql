-- Гаджилы Орхан

---------------------------------------------------------------------------------------------------------------------------------
-- 1 Посчитайте общую сумму продаж в США в 1 квартале 2012 года? Решить 2-мя  способами Джойнами и Подзапросами
-- Джоин
SELECT sum(si.UnitPrice * si.Quantity)
FROM sales s
LEFT JOIN sales_items si
ON s.SalesId = si.SalesId
WHERE s.ShipCountry = 'USA'
  AND s.SalesDate BETWEEN '2012-01-01' AND '2012-03-31'

-- Подзапрос (некоррелированный)
SELECT sum(UnitPrice * Quantity)
FROM sales_items
WHERE SalesId IN
(
	SELECT SalesId
	FROM sales
	WHERE ShipCountry = 'USA'
	  AND SalesDate BETWEEN '2012-01-01' AND '2012-03-31'
)

-- Подзапрос (коррелированный)
SELECT sum(UnitPrice * Quantity)
FROM sales_items si
WHERE SalesId IN
(
	SELECT SalesId
	FROM sales s
	WHERE ShipCountry = 'USA'
	  AND s.SalesId = si.SalesId
	  AND s.SalesDate BETWEEN '2012-01-01' AND '2012-03-31'
)


---------------------------------------------------------------------------------------------------------------------------------
-- 2 Покажите имена клиентов, которых нет среди работников. Решить 3-мя способами: подзапросами, джойнами и логическим вычитанием.
-- Подзапрос (некоррелированный)
SELECT DISTINCT FirstName
FROM customers
WHERE FirstName NOT IN
(
	SELECT FirstName
	FROM employees
)

-- Джоин
SELECT DISTINCT c.FirstName
FROM customers c
LEFT JOIN employees e 
ON c.FirstName = e.FirstName
WHERE e.FirstName IS NULL

-- Логическое вычитание
SELECT DISTINCT c.FirstName
FROM customers c

EXCEPT

SELECT FirstName
FROM employees


---------------------------------------------------------------------------------------------------------------------------------
-- 3 Теор вопрос
/*
	Вернет ли данный запрос  одинаковый результат?  Да или НЕТ. 
	Если  ДА. Объяснить почему.
	Если НЕТ. Объяснить почему. Какой  запрос вернет больше строк ?

 	select *
 	from T1 LEFT JOIN T2
		ON T1.column1=T2.column1
	 where   T1.column1=0
 	
	 select *
	 from T1 LEFT JOIN T2
		ON T1.column1=T2.column1 and   T1.column1=0
 */

-- ОТВЕТ
/*
Второй запрос вернет не меньше строк, чем первый.
1)	В первом запросе после джоина отбираются некоторые строки (условие WHERE).
	Если все строки T1.column1 равны нулю, то выполнение условия WHERE не уменьшит кол-во строк в результирующей таблице.
	Иначе, строк будет меньше.
2)	Во втором запросе джоин происходит по другому правилу, но зато теперь нет условия WHERE, которое убрало бы часть строк.
	Поэтому, в итоге строк во втором запросе будет либо столько же, либо больше, чем в первом запросе.
*/


---------------------------------------------------------------------------------------------------------------------------------
-- 4 Посчитайте количество треков в каждом альбоме. В результате должно быть:  имя альбома и кол-во треков. Решить  2-мя способами: подзапросом и джойнами
-- Джоин
SELECT
	 --p.PlaylistId,
	 p.Name
	,COUNT(pt.TrackId) as TrackCount
FROM playlists p
LEFT JOIN playlist_track pt
ON p.PlaylistId = pt.PlaylistId
GROUP BY p.PlaylistId, p.Name
ORDER BY p.PlaylistId

-- Подзапрос (коррелированный)
SELECT
	 p.Name
	,(
		SELECT COUNT(pt.TrackId)
		FROM playlist_track pt
		WHERE pt.PlaylistId = p.PlaylistId
	 ) as TrackCount
	
FROM playlists p


---------------------------------------------------------------------------------------------------------------------------------
-- 5 Покажите фамилию и имя покупателей немцев сделавших заказы в 2009 году, товары которых были отгружены в город Берлин?
SELECT
	 DISTINCT
	 c.FirstName
	,c.LastName
FROM customers c
LEFT JOIN sales s 
ON c.CustomerId = s.CustomerId 

WHERE c.Country = 'Germany'
  AND s.ShipCity = 'Berlin'
  AND STRFTIME('%Y', s.Salesdate) = '2009'


---------------------------------------------------------------------------------------------------------------------------------
-- 6 Покажите фамилии клиентов которые  купили больше 30 музыкальных треков ? Решить  задачу ,как минимум, 2-мя способами: джойнами и подзапросами
-- Джоин
SELECT
	 c.LastName
FROM customers c
LEFT JOIN sales s ON c.CustomerId = s.CustomerId
LEFT JOIN sales_items si ON s.SalesId = si.SalesId
GROUP BY
	 c.CustomerId
	,c.LastName
HAVING COUNT(si.TrackId) > 30
  
-- Подзапрос (некоррелированыый + коррелированный)
SELECT
	 c.LastName
FROM customers c
WHERE c.CustomerId IN
	(
		SELECT
			 CustomerId
		FROM
		(
			SELECT
				 s.CustomerId
				,(
					SELECT COUNT(si.TrackId)
					FROM sales_items si
					WHERE s.SalesId = si.SalesId
				 ) as TrackCountInSale
			FROM sales s
		 ) T1
		 GROUP BY
		 	 CustomerId
		 HAVING SUM(TrackCountInSale) > 30
	)


---------------------------------------------------------------------------------------------------------------------------------
-- 7 В базе есть таблица музыкальных треков и жанров Назовите среднюю стоимстость музыкального трека в каждом жанре?
SELECT
	 g.Name
	,AVG(t.UnitPrice)
FROM genres g
LEFT JOIN tracks t
ON g.GenreId = t.GenreId
GROUP BY
	 g.Name
	,g.GenreId
ORDER BY
	 g.GenreId


---------------------------------------------------------------------------------------------------------------------------------
--8 В базе есть таблица музыкальных треков и жанров. Покажите жанры у которых средняя стоимость одного трека больше 1-го рубля
SELECT
	 g.Name
FROM genres g
LEFT JOIN tracks t
ON g.GenreId = t.GenreId
GROUP BY
	 g.Name
	,g.GenreId
HAVING
	 AVG(t.UnitPrice) > 1.0
ORDER BY
	 g.GenreId
	 
	 
	 
	 
