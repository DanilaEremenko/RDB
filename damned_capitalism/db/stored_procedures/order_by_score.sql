drop function if exists order_by_score();
create function order_by_score() returns table
                                                             (
                                                                    first_name varchar,
                                                                    second_name varchar,
                                                                    score integer
                                                             )
as
$$
begin
    for first_name, second_name, score in
        select p.first_name,p.second_name,sum(it.value) as score
        from person_item pit
          join item it on pit.item_id = it.id
          join person p on pit.person_id = p.id
          group by p.first_name,p.second_name
          order by score desc
        loop
            return next;
        end loop;
end;
$$ language plpgsql;
