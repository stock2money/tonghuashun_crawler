CREATE DATABASE if not EXISTS mydb;
use mydb;


create table if not exists recommend(
    last_close varchar(10) not NULL,
	today_open varchar(10) not null,
    last_price varchar(10) not null,
    `change` varchar(20) not null,
    change_rate varchar(20) not null,
    `code` varchar(20) not null,
    `date` varchar(20) not null,
    `name` varchar(20) not null,
    strategy varchar(20) not null,
    primary key(code, strategy)
) charset=utf8;

create table if not exists strategy(
    strategy varchar(10) not NULL,
	successRate int not null,
    operation text not null,
    `usage` text not null,
    primary key(strategy)
) charset=utf8;