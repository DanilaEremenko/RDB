/*---------------- delete all tables and roles ------------------------*/
drop table cook_condition cascade;
drop table market_name cascade;
drop table product_type cascade;
drop table way_of_cooking cascade;
drop table recipe cascade;
drop table product cascade;
drop table refregerator cascade;
drop table recipe_product cascade;
drop table recipe_product_num cascade;

revoke all on database refregerator from refregerator_manager;
drop role refregerator_manager;