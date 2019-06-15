drop function if exists get_item_person();
create function get_item_person() returns table
                                                             (
                                                                    first_name varchar,
                                                                    second_name varchar,
                                                                    item_id integer,
                                                                    item_price integer,
                                                                    item_value integer
                                                             )
as
$$
begin
    for first_name, second_name, item_id, item_price, item_value in
        select p.first_name, p.second_name, it.id, it.price, it.value
        from person_item pit
          join item it on pit.item_id = it.id
          join person p on pit.person_id = p.id
          order by p.id,it.price,it.value
        loop
            return next;
        end loop;
end;
$$ language plpgsql;
