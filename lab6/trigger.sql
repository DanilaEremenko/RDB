/*
Триггер для автоматического заполнения ключевого поля.
*/

drop function if exists new_id() cascade;
create function new_id() returns trigger
as
$$
begin
    select max(id) + 1 into new.id from refregerator;
    return new;
end;
$$ language plpgsql;

/*TODO maybe someday
select coalesce(min(nullif(r1.id - 1, r2.id)), max(r2.id) + 1) as min_free_id
from refregerator r1
         left join (select id from refregerator) r2 on r1.id - 1 = r2.id;
*/

create trigger new_id_trig
    before insert
    on refregerator
    for each row
execute procedure new_id();

/*
Триггер для контроля целостности данных в подчиненной таблице при удалении/изменении записей в главной таблице
*/

drop function if exists delete_market_name() cascade;
create function delete_market_name() returns trigger
as
$$
declare
    market_name_id_ integer;
begin
    select id into market_name_id_ from market_name where name = old.name;
    delete from refregerator where market_name_id = market_name_id_;
    return old;
end;
$$ language plpgsql;

create trigger check_delete
    before update or delete
    on market_name
    for each row
execute procedure delete_market_name();


/*
Автоматически заполнять дату покупки (текущей) при добавлении записей в холодильник.
*/

drop function if exists fix_buying_date() cascade;

create function fix_buying_date() returns trigger
as
$$
declare
begin
    new.buying_date = current_date;
    return new;
end;
$$ language plpgsql;


create trigger fix_byuing_date_trig
    before insert or update
    on refregerator
    for each row
execute procedure fix_buying_date();


/*
Проверять дубли при добавлении продуктов в рецепт. При дублировании выбрасывать исключение.
*/
drop function if exists check_repeat_in_recipe_product() cascade;
create function check_repeat_in_recipe_product() returns trigger
as
$$
begin
    if new.product_id in (select product_id from recipe_product where recipe_id = new.recipe_id)
    then
        RAISE EXCEPTION 'product % already exist in recipe %',new.product_id,new.recipe_id;
    end if;
    return null;
end;
$$ language plpgsql;

create trigger check_repeat_in_recipe_product_trig
    before insert or update
    on recipe_product
    for each row    
execute procedure check_repeat_in_recipe_product();



