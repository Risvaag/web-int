begin;

create schema data;

create table data.articles (
  id                      serial primary key,
  url                     text,
  title                   text,
  author                  text,
  description             text,
  image                   text,
  publushed_time          text,
  modified_time           text,
  category                text,
  keywords                text,
  body                    text
);

commit;
