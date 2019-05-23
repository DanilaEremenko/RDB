/*Сделайте выборку всех данных из каждой таблицы*/
select * from product_type;
select * from cook_condition;
select * from way_of_cooking;
select * from market_name;
select * from product;
select * from recipe;
select * from refregerator;
select * from recipe_product;


/*Сделайте выборку данных из одной таблицы при нескольких условиях,
  с использованием логических операций, LIKE, BETWEEN, IN (не менее 3-х разных примеров)*/
select * from product where priority in (1,2);
select * from refregerator where price between 100 and 200;
select * from recipe where name like '%sal%';

/*Создайте в запросе вычисляемое поле*/
select max(price) from refregerator;

/*Сделайте выборку всех данных с сортировкой по нескольким полям*/
select id,price,disc_price from refregerator order by price,disc_price;

/*Создайте запрос, вычисляющий несколько совокупных характеристик таблиц*/
select min(day_before_expiring),max(price),min(price) from refregerator;

/*Сделайте выборку данных из связанных таблиц (не менее двух примеров)*/
select amount,p.name,mn.name from refregerator
    join product p on refregerator.product_id = p.id
    join market_name mn on refregerator.market_name_id = mn.id
    order by mn.name,amount;

/*Создайте запрос, рассчитывающий совокупную характеристику с использованием группировки,
  наложите ограничение на результат группировки*/
SELECT mn.name,price
FROM refregerator
join market_name mn on refregerator.market_name_id = mn.id
WHERE disc_price>price and amount > 2
GROUP BY mn.name,price;
