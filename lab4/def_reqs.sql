-------------------------- ОБЩАЯ ЧАСТЬ ---------------------------------------
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


----------------------------------------------------------------------------------------
---------------------------- ИНДВИДУАЛЬНЫЕ ЗАДАНИЯ -------------------------------------

------------------------------------------------------------------------------
/*1.Вывести порядок приготовления блюда и ингридиенты*/
select r.name recipe, wc.name how_to_cook, p.name products,product_amount
from recipe_product rp
         join recipe r on rp.recipe_id = r.id
         join way_of_cooking wc on r.way_of_cooking_id = wc.id
         join product p on rp.product_id = p.id
order by r.name;

------------------------------------------------------------------------------
/*2.Вывести блюда, которые есть в холодильнике, но не входят в рецепты*/
select r.id, p.name
from refregerator r
         join product p on r.product_id = p.id
where p.id not in (select rp.product_id from recipe_product rp);

------------------------------------------------------------------------------
/*3.Вывести рецепты, для приготовления блюд по которым не хватает не более 3-х ингридиентов.*/
select *
from (select rec_full.recipe, count(product_full) - count(product_from_refr) as missed_num
      from (
            (select rec.name as recipe, p.name as product_from_refr
             from refregerator refr
                      join product p on refr.product_id = p.id --взяли продукты только из холодильника
                      join recipe_product rp on p.id = rp.product_id --взяли рецепты для этих продуктов
                      join recipe rec on rp.recipe_id = rec.id --взяли имя рецепта
             group by rec.name,-- чтобы рецепт показывался,
                      p.name   -- если хотя бы 1 продукт найден ()
             order by rec.name, p.name) rec_in_refr
               right join
           (select rec.name as recipe, p.name as product_full
            from recipe_product rp
                     join recipe rec on rp.recipe_id = rec.id -- взяли названия все рецептов
                     join product p on rp.product_id = p.id -- взяли продукты для этих рецептов
            order by rec.name, p.name) rec_full
           on rec_in_refr.recipe = rec_full.recipe
               and rec_in_refr.product_from_refr = rec_full.product_full)
      group by rec_full.recipe) missed_pr
where missed_num <= 3;