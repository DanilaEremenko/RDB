-- update recipe_product_num table
drop table if exists recipe_product_num;

create table recipe_product_num
(

    recipe_id   integer not null,
    foreign key (recipe_id) references recipe (id),

    product_num integer not null


);

insert into recipe_product_num
select recipe_id, count(recipe_id)
from recipe_product
group by recipe_id
order by recipe_id;
