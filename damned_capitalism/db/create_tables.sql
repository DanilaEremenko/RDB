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
    second_name varchar(100) not null
);
-----------------------------------------------------------
create table person_item
(
    id        serial primary key,
    person_id integer not null,
    item_id   integer not null,

    foreign key (person_id) references person (id),
    foreign key (item_id) references item (id)
);

-----------------------------------------------------------
create table party
(
    party_id       integer      not null,
    account        integer      not null,
    max_time       integer      not null,
    first_name     varchar(100) not null,
    second_name    varchar(100) not null,
    score          integer      not null,
    spended_money  integer      not null,
    remained_money integer      not null

);


/*------------------------------- create manager -------------------------*/
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
