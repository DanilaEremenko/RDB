/*------------------------------- examples:ready, not ready --------------------------------*/
create table cook_condition
(
    id   serial primary key,
    name varchar(15) not null unique
);

/*-------------------- examples:okay,lenta,pyatorochka --------------------------------------*/
create table market_name
(
    id   serial primary key,
    name varchar(15) not null unique
);

/* --------------------- examples:fruit, vegetable, meat, fish ------------------------------*/
create table product_type
(
    id   serial primary key,
    name varchar(15) not null unique
);


/* ------------------- examples:fry, boil, bake --------------------------------------------*/
create table way_of_cooking
(
    id   serial primary key,
    name varchar(15) not null unique

);

/*----------------------------------------- main item --------------------------------------*/
create table product
(
    id                serial primary key,
    name              varchar(15) not null unique,
    mark              varchar(15) not null,
    priority          integer,/*for absent products*/

    cook_condition_id integer,
    product_type_id   integer,

    foreign key (cook_condition_id) references cook_condition (id),
    foreign key (product_type_id) references product_type (id)

);

/*------------------------------ many-to-many linking table ------------------------------*/
create table way_of_cooking_product
(
    id                serial primary key,

    way_of_cooking_id integer,
    foreign key (way_of_cooking_id) references way_of_cooking (id),
    product_id        integer


);


/*----------------------------------- products container ----------------------------*/
create table refregerator
(
    id                  serial primary key,
    product_id          integer,
    market_name_id      integer,
    price               integer,
    disc_price          integer, /*discount price*/
    buying_date         date,
    day_before_expiring integer,
    amount              integer,

    foreign key (product_id) references product (id),
    foreign key (market_name_id) references market_name (id)
);


/*----------------------------- some enum-tables initializing --------------------------------------*/

alter table way_of_cooking_product
    add foreign key (product_id) references product (id);

/*cook_coniditon init*/
insert into cook_condition
values (1, 'ready');
insert into cook_condition
values (2, 'not ready');

/*market_name init*/
insert into market_name
values (1, 'okay');
insert into market_name
values (2, 'pyatorochka');

/*product_type init*/
insert into product_type
values (1, 'fruit');
insert into product_type
values (2, 'vegetable');
insert into product_type
values (3, 'meat');
insert into product_type
values (4, 'fish');
insert into product_type
values (5, 'garnish');
insert into product_type
values (6, 'sauce');
insert into product_type
values (7, 'milk-product');
insert into product_type
values (8, 'starter');

/*way_of_cooking init*/
insert into way_of_cooking
values (1, 'fry');
insert into way_of_cooking
values (2, 'boil');
insert into way_of_cooking
values (3, 'bake');



/*--------------------- some common products initializing --------------------------------------*/

/*product 1 example
 pasta, bariila, high-priority, not ready, garnish
 boil
 */
insert into product
values (1, 'pasta', 'barilla', 2, 2, 5);
insert into way_of_cooking_product
values (1, 2, 1);


/*product 2 example
 narsharab, kinto, high-priority, ready, sauce
 */
insert into product
values (2, 'narsharab', 'kinto', 2, 1, 6);


/*product 3 example
 yogurt, epica, high-priority, ready, milk-product
 */
insert into product
values (3, 'yogurt', 'epica', 2, 1, 7);


/*product 4 example
 loaf, karavai, hight-priority, ready, started
*/
insert into product
values (4, 'loaf', 'karavai', 2, 1, 8);



/*----------------------- refregerator filling example --------------------------------------*/
/*id, loaf, okay, 59 rub, 45 rub, today, 14 days, 2 packs*/
insert into refregerator
values (1, 4, 1, 59, 45, current_date, 14, 2);

/*id, loaf, okay, 304 rub, 220 rub, today, 700 days, 2 bottle*/
insert into refregerator
values (2, 2, 1, 304, 220, current_date, 700, 1);

/*id, yogurt, okay, 50 rub, 39 rub, today, 32 days, 4 packs */
insert into refregerator
values (3, 3, 1, 50, 39, current_date, 32, 4);

/*todo if not exist*/
create role refregerator_manager with login password '1234';

/*------------ grants for manager -----------------*/

grant select on table cook_condition to refregerator_manager;
grant references on table cook_condition to refregerator_manager;

grant select on table product_type to refregerator_manager;
grant references on table product_type to refregerator_manager;

grant select on table way_of_cooking to refregerator_manager;
grant references on table way_of_cooking to refregerator_manager;

grant select on table market_name to refregerator_manager;
grant references on table market_name to refregerator_manager;



grant select on table product to refregerator_manager;
grant insert on table product to refregerator_manager;
grant references on table product to refregerator_manager;
grant delete on table product to refregerator_manager;


grant select on table refregerator to refregerator_manager;
grant insert on table refregerator to refregerator_manager;
grant delete on table refregerator to refregerator_manager;

