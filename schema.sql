-- noinspection SqlNoDataSourceInspectionForFile
drop table if exists files;
create table files (
  file text primary key not null,
  b2 text,
  time int,
  accessed int
);