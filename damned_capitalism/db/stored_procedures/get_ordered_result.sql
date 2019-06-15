drop function if exists get_ordered_result();
create function get_ordered_result() returns table
                                             (
                                                 first_name varchar,
                                                 second_name varchar,
                                                 sum_score integer,
                                                 sum_price integer
                                             )
as
$$
begin
    for first_name, second_name, sum_score, sum_price in
        select p.first_name, p.second_name, sum(it.value) as sum_score, sum(price) as sum_price
        from person_item pit
                 join item it on pit.item_id = it.id
                 join person p on pit.person_id = p.id
        group by p.first_name, p.second_name
        order by sum_score desc
        loop
            return next;
        end loop;
end;
$$ language plpgsql;
