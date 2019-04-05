/*delete all tables
drop table cook_condition cascade;
drop table market_name cascade;
drop table product_type cascade;
drop table way_of_cooking cascade;
drop table product cascade;
drop table refregerator cascade;
drop table way_of_cooking_product cascade;
*/


/*examples:ready, not ready*/
CREATE TABLE Cook_condition
(
	id SERIAL PRIMARY KEY,
	name VARCHAR(15) NOT NULL UNIQUE
);

/*examples:okay,lenta,pyatorochka*/
CREATE TABLE Market_name
(
	id SERIAL PRIMARY KEY,
	name VARCHAR(15) NOT NULL UNIQUE
);

/*examples:fruit, vegetable, meat, fish*/
CREATE TABLE Product_type
(
	id SERIAL PRIMARY KEY,
	name VARCHAR(15) NOT NULL UNIQUE
);


/*examples:fry, boil, bake*/
CREATE TABLE Way_of_cooking
(
	id SERIAL PRIMARY KEY,
	name VARCHAR(15) NOT NULL UNIQUE

);

/*main item*/
CREATE TABLE Product
(
	id SERIAL PRIMARY KEY,
        name VARCHAR(15) NOT NULL UNIQUE,
	mark VARCHAR(15) NOT NULL,
	priority INTEGER,/*for absent products*/

	cook_condition_id INTEGER,
	product_type_id INTEGER,
	
	FOREIGN KEY (cook_condition_id)  REFERENCES Cook_condition (id),
	FOREIGN KEY (product_type_id) REFERENCES Product_type (id)

);

/*many-to-many linking table*/
CREATE TABLE Way_of_cooking_product
(
        id SERIAL PRIMARY KEY,

        way_of_cooking_id INTEGER,
        FOREIGN KEY (way_of_cooking_id) REFERENCES Way_of_cooking (id),
        product_id INTEGER


);



/*products container*/
CREATE TABLE Refregerator
(
	id SERIAL PRIMARY KEY,
	product_id INTEGER,
	market_name_id INTEGER,
	price INTEGER,
	disc_price  INTEGER,	/*discount price*/
	day_of_buying INTEGER,
        expire_date INTEGER,
        amount INTEGER,
	
	FOREIGN KEY(product_id) REFERENCES Product(id),
	FOREIGN KEY (market_name_id) REFERENCES Market_name (id)
);

alter table Way_of_cooking_product
ADD FOREIGN KEY (product_id) REFERENCES Product(id);
	
/*cook_coniditon init*/
insert into cook_condition values (1,'ready');
insert into cook_condition values (2,'not ready');

/*market_name init*/
insert into market_name values (1, 'okay');
insert into market_name values (2, 'pyatorochka');

/*product_type init*/
insert into product_type values(1,'fruit');
insert into product_type values(2,'vegetable');
insert into product_type values(3,'meat');
insert into product_type values(4,'fish');
insert into product_type values(5,'garnish');
insert into product_type values(6,'sauce');
insert into product_type values(7,'milk-product');

/*way_of_cooking init*/
insert into way_of_cooking values (1,'fry');
insert into way_of_cooking values (2,'boil');
insert into way_of_cooking values (3,'bake');



/*product 1 example
 pasta, bariila, high-priority, not ready, garnish
 boil
 */
insert into product values (1,'pasta','barilla',2,2,5);
insert into way_of_cooking_product values (1,2,1);


/*product 2 example
 narsharab, kinto, high-priority, ready, sauce
 */
insert into product values (2,'narsharab','kinto',2,1,6);


/*product 3 example
 yogurt, epica, high-priority, ready, milk-product
 */
insert into product values (3, 'yogurt','epica',2,1,7);

/*product 4 example
 
 */
