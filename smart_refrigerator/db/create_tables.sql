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

/*------------------------------------ table with clients ------------------------------*/
create table client
(
  id          serial primary key,
  first_name  varchar(30) not null,
  second_name varchar(30) not null,
  account     integer     not null

);

/*----------------------------------- products container ----------------------------*/
create table refrigerator
(
  id                  serial primary key,
  client_id           integer not null,
  product_id          integer not null,
  market_name_id      integer not null,
  price               integer not null,
  disc_price          integer not null, /*discount price*/
  buying_date         date    not null,
  day_before_expiring integer not null,
  amount              integer not null,

  foreign key (client_id) references client (id),
  foreign key (product_id) references product (id),
  foreign key (market_name_id) references market_name (id)
);




/*----------------------------- enum-tables initializing --------------------------------------*/
/*------------- cook_coniditon init -------------*/
insert into cook_condition
values (default, 'ready');

insert into cook_condition
values (default, 'not ready');

/*------------- market_name init -------------*/
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


/*------------- product_type init -------------*/
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

/*------------- way_of_cooking init -------------*/
insert into way_of_cooking
values (default, 'fry');

insert into way_of_cooking
values (default, 'boil');

insert into way_of_cooking
values (default, 'bake');


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
