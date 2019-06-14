-----------------------------------------------------------
create table item
(
    id    serial primary key,
    name  varchar(100) not null,
    price integer      not null,
    value integer      not null
);

-----------------------------------------------------------
create table person
(
    id          serial primary key,
    first_name  varchar(100) not null,
    second_name varchar(100) not null,
    account     integer      not null
);
-----------------------------------------------------------
create table client_item
(
    id        serial primary key,
    client_id integer not null,
    item_id   integer not null,

    foreign key (client_id) references person (id),
    foreign key (item_id) references item (id)
);

-----------------------------------------------------------
create table hall_of_fame
(
    id          serial primary key,
    first_name  varchar(100) not null,
    second_name varchar(100) not null,
    spend_money integer      not null


);


/*------------------------------- create refregerator manager -------------------------*/
create
    user
    manager
    with
    login
    password
        '1234';

grant
    postgres
    to
    manager;
