create database "tiripode";
\c tiripode;

drop table if exists inflection;
drop table if exists form;
drop table if exists dict_entry;

create table if not exists dict_entry (
    entryid serial primary key,
    word varchar(50) not null,
    entrydefinition text not null,
    category varchar(20),
    stem varchar(100)
);

create table if not exists form (
    formid serial primary key,
    -- case and number are reserved words :'(
    formdeclension varchar(50) not null,
    formcase varchar(50) not null,
    formgender varchar(50) not null,
    formnumber varchar(50) not null,
    formending varchar(20) not null
);

create table if not exists inflection (
    inflectionid serial primary key,
    inflection varchar(50) not null,
    form int references form(formid) not null,
    dict_entry int references dict_entry(entryid) not null,
    uncertaingender boolean not null
);
