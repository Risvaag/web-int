begin;

create schema adressa;

create table adressa.events (
  id                      serial primary key,
  active_time             int,
  author                  text,
  canonical_url           text,
  category                text,
  city                    text,
  country                 text,
  device_type             text,
  event_id                int,
  cx_id                   text,
  keywords                text,
  os                      text,
  publishtime             text,
  query                   text,
  referrer_host_class     text,
  referrer_search_engine  text,
  referrer_social_network text,
  referrer_query          text,
  referrer_url            text,
  region                  text,
  session_start           boolean,
  session_stop            boolean,
  cx_time                 int,
  title                   text,
  url                     text,
  user_id                 text
);

commit;
