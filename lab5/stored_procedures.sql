/*--------------------------------------------------------------------------
1. Вывести список блюд и массу каждого, которые можно приготовить из содержимого холодильника
  return
        table:
            recipe_id | recipe_name | missed | weight
*/
drop function if exists available_recipes(max_missed int);
create function available_recipes(max_missed int) returns table
                                                          (
                                                              rec_id int,
                                                              rec_name varchar,
                                                              missed_num int,
                                                              rec_weight int
                                                          )
as
$$
begin
    for rec_id, rec_name, missed_num, rec_weight in
        select *
        from (select recipe_id,
                     recipe_name,
                     sum(abs(missed_amount)) as product_need,
                     r.weight
              from get_necessary_products_for_recipes()
                       join recipe r on r.id = recipe_id
              group by recipe_id, recipe_name, r.weight
              order by recipe_id
             ) recipe_with_missed
        where product_need <= max_missed
        loop
            return next;
        end loop;
end;
$$ language plpgsql;

/*------------------------ example ------------------------------------------

select *
from available_recipes(0);

*/

/*----------------------------------------------------------------------------------------*/

/*--------------------------------------------------------------------------
2. Сформировать заказ на продукты по списку рецептов
    return
        table:
            recipe_id | recipe_name | product_need | missed_amount
*/
drop function if exists get_necessary_products_for_recipes();
create function get_necessary_products_for_recipes() returns table
                                                             (

                                                                 recipe_id int,
                                                                 recipe_name varchar,
                                                                 product_need varchar,
                                                                 missed_amount int

                                                             )
as
$$
begin
    for recipe_id, recipe_name, product_need,missed_amount in
        select r.id, r.name, p.name, coalesce(rp.product_amount - ref_prod.amount, rp.product_amount)
        from recipe_product rp
                 join recipe r on rp.recipe_id = r.id
                 join product p on rp.product_id = p.id
                 left join (select p.name, amount
                            from refregerator refr
                                     join product p on refr.product_id = p.id) ref_prod on p.name = ref_prod.name
        order by r.id, p.name
        loop
            return next;
        end loop;
end;
$$ language plpgsql;


/*------------------------ example ------------------------------------------

select *
from get_necessary_products_for_recipes()
where recipe_name in (select r.name
                      from recipe_product rp
                               join recipe r on rp.recipe_id = r.id
                      group by r.id
                      order by r.id
                      limit 2)
order by recipe_id;

*/