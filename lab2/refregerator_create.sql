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
    name              varchar(15) not null,
    mark              varchar(15) not null,
    priority          integer     not null,/*for absent products*/

    cook_condition_id integer     not null,
    product_type_id   integer     not null,

    foreign key (cook_condition_id) references cook_condition (id),
    foreign key (product_type_id) references product_type (id)

);


/*----------------------------- available recipes -----------------------------------------*/
create table recipe
(
    id                serial primary key,
    name              varchar(50) not null,
    weight            integer     not null,

    way_of_cooking_id integer     not null,
    foreign key (way_of_cooking_id) references way_of_cooking (id)

);


/*------------------------------ many-to-many linking table ------------------------------*/
create table recipe_product
(
    id             serial primary key,

    recipe_id      integer not null,
    foreign key (recipe_id) references recipe (id),

    product_id     integer not null,
    foreign key (product_id) references product (id),
    product_amount integer not null

);


/*----------------------------------- products container ----------------------------*/
create table refregerator
(
    id                  serial primary key,
    product_id          integer not null,
    market_name_id      integer not null,
    price               integer not null,
    disc_price          integer not null, /*discount price*/
    buying_date         date    not null,
    day_before_expiring integer not null,
    amount              integer not null,

    foreign key (product_id) references product (id),
    foreign key (market_name_id) references market_name (id)
);



/*----------------------------- enum-tables initializing --------------------------------------*/
/*cook_coniditon init*/
insert into cook_condition
values (default, 'ready');

insert into cook_condition
values (default, 'not ready');

/*market_name init*/
insert into market_name
values (default, 'OKAY');

insert into market_name
values (default, 'PYATOROCHKA');

insert into market_name
values (default, 'LENTA');

insert into market_name
values (default, 'MAGNIT');

insert into market_name
values (default, 'MISTER LOPATA');

insert into market_name
values (default, 'MISHA KOSINKA');


/*product_type init*/
insert into product_type
values (default, 'fruit');

insert into product_type
values (default, 'vegetable');

insert into product_type
values (default, 'meat');

insert into product_type
values (default, 'fish');

insert into product_type
values (default, 'garnish');

insert into product_type
values (default, 'sauce');

insert into product_type
values (default, 'milk-product');

insert into product_type
values (default, 'starter');

/*way_of_cooking init*/
insert into way_of_cooking
values (default, 'fry');

insert into way_of_cooking
values (default, 'boil');

insert into way_of_cooking
values (default, 'bake');


/*--------------------- some common products initializing --------------------------------------*/

/*product 1 example
 pasta, bariila, high-priority, not ready, garnish
 boil
 */
insert into product
values (default, 'pasta', 'barilla', 2, 2, 5);


/*product 2 example
 narsharab, kinto, high-priority, ready, sauce
 */
insert into product
values (default, 'narsharab', 'kinto', 2, 1, 6);


/*product 3 example
 yogurt, epica, high-priority, ready, milk-product
 */
insert into product
values (default, 'yogurt', 'epica', 2, 1, 7);


/*product 4 example
 loaf, karavai, hight-priority, ready, started
*/
insert into product
values (default, 'loaf', 'karavai', 2, 1, 8);


/*----------------------- refregerator filling example --------------------------------------*/
/*id, loaf, okay, 59 rub, 45 rub, today, 14 days, 2 packs*/
insert into refregerator
values (default, 4, 1, 59, 45, current_date, 14, 2);

/*id, loaf, okay, 304 rub, 220 rub, today, 700 days, 2 bottle*/
insert into refregerator
values (default, 2, 1, 304, 220, current_date, 700, 1);

/*id, yogurt, okay, 50 rub, 39 rub, today, 32 days, 4 packs */
insert into refregerator
values (default, 3, 1, 50, 39, current_date, 32, 4);


/*------------------------------- create refregerator manager -------------------------*/
create
    user
    refregerator_manager
    with
    login
    password
        '1234';

grant postgres to refregerator_manager;
