/*-------------------- examples:okay,lenta,pyatorochka --------------------------------------*/
create table market
(
    id     serial primary key,
    name   varchar(15) not null unique,
    rating int         not null

);


/* --------------------- examples:fruit, vegetable, meat, fish ------------------------------*/
create table food_type
(
    id   serial primary key,
    name varchar(15) not null unique
);


/*----------------------------------------- main item --------------------------------------*/
create table food
(
    id                serial primary key,
    name              varchar(15) not null,
    mark              varchar(15) not null,
    priority          integer     not null,/*for absent products*/

    food_type_id      integer     not null,

    foreign key (food_type_id) references food_type (id)

);

/*------------------------------------ table with clients ------------------------------*/
create table client
(
    id              serial primary key,
    first_name      varchar(30) not null,
    second_name     varchar(30) not null,
    account         integer     not null,
    salary          integer     not null,
    employment      varchar(50),
    education       varchar(50),
    day_without_eat integer     not null

);

/*----------------------------------- products container ----------------------------*/
create table client_refrigerator
(
    id                  serial primary key,
    client_id           integer not null,
    food_id          integer not null,
    market_id           integer not null,
    price               integer not null,
    disc_price          integer not null, /*discount price*/
    buying_date         date    not null,
    day_before_expiring integer not null,
    amount              integer not null,

    foreign key (client_id) references client (id),
    foreign key (food_id) references food (id),
    foreign key (market_id) references market (id)
);


create table market_refrigerator
(
    id                  serial primary key,
    market_id           integer not null,
    food_id          integer not null,
    price               integer not null,
    disc_price          integer not null,
    day_before_expiring integer not null,
    amount              integer not null,

    foreign key (market_id) references market (id),
    foreign key (food_id) references food (id)


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
