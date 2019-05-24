------------------------------------------------------------------------------
/*Сделайте выборку всех данных из каждой таблицы*/
select *
from product_type;

select *
from cook_condition;

select *
from way_of_cooking;

select *
from market_name;

select *
from product;

select *
from recipe;

select *
from refregerator;

select *
from recipe_product;


------------------------------------------------------------------------------
/*Сделайте выборку данных из одной таблицы при нескольких условиях,
  с использованием логических операций, LIKE, BETWEEN, IN (не менее 3-х разных примеров)*/
select *
from product
where priority in (1, 2);

select *
from refregerator
where price between 100 and 200;

select *
from recipe
where name like '%sal%';

------------------------------------------------------------------------------
/*Создайте в запросе вычисляемое поле*/
select max(price)
from refregerator;

------------------------------------------------------------------------------
/*Сделайте выборку всех данных с сортировкой по нескольким полям*/
select id, price, disc_price
from refregerator
order by price, disc_price;

------------------------------------------------------------------------------
/*Создайте запрос, вычисляющий несколько совокупных характеристик таблиц*/
select min(day_before_expiring) as expire,
       max(price)               as max_price,
       min(price)               as min_price
from refregerator;

------------------------------------------------------------------------------
/*Сделайте выборку данных из связанных таблиц (не менее двух примеров)*/
/*Продукты лежащие в холодильнике отсортированные по магазинам и количеству*/
select amount, p.name, mn.name
from refregerator
         join product p on refregerator.product_id = p.id
         join market_name mn on refregerator.market_name_id = mn.id
order by mn.name, amount;

------------------------------------------------------------------------------
/*Создайте запрос, рассчитывающий совокупную характеристику с использованием группировки,
  наложите ограничение на результат группировки*/
/*Цены в каждом магазине*/
select mn.name,
       max(price)      as max_price,
       min(price)      as min_price,
       max(disc_price) as max_dprice,
       min(disc_price) as min_dprice
from refregerator
         join market_name mn on refregerator.market_name_id = mn.id
where disc_price > price
  and amount > 2
group by mn.name;

------------------------------------------------------------------------------
/*Придумайте и реализуйте пример использования вложенного запроса*/
/*Все овощи в холодильнике*/
select pname, veg.name, priority
from refregerator
         join
     (select p.name as pname, p.id, pt.name, priority
      from product as p
               join product_type pt on p.product_type_id = pt.id
      where pt.name = 'vegetable') as veg on product_id = veg.id;


------------------------------------------------------------------------------
/*С помощью оператора INSERT добавьте в каждую таблицу по одной записи*/
insert into product_type
values ((select max(id) + 1 from product_type), 'new_pt');

/*all inserts you can find in lab2/refregerator_create.sql*/

-- TODO how to do something like
-- DO
-- BEGIN
--    FOR tab_name IN market_name,product_type LOOP
--       delete from tab_name where name like 'new_%';
--    END LOOP;
-- END

insert into recipe_product
        (select max(id) from recipe_product as new_id);

------------------------------------------------------------------------------
/*С помощью оператора UPDATE измените значения нескольких полей у всех записей,
  отвечающих заданному условию*/
/*vegetable priority = */
update product
set priority=1
where product_type_id
          in (select id from product_type where name = 'vegetable');


------------------------------------------------------------------------------
/*С помощью оператора DELETE удалите запись,
  имеющую максимальное (минимальное) значение некоторой совокупной характеристики*/
delete
from refregerator
where price = max(price);
delete
from refregerator
where day_before_expiring = 0;

------------------------------------------------------------------------------
/*С помощью оператора DELETE удалите записи в главной таблице, на которые
  не ссылается подчиненная таблица (используя вложенный запрос)*/
delete
from recipe_product
where id = (select max(id) from recipe_product);
