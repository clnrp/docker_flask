create database flaskdb;
\c flaskdb;

CREATE TABLE if not exists userdb(
  id BIGSERIAL PRIMARY KEY,
  name varchar(200) DEFAULT NULL,
  email varchar(100) DEFAULT NULL,
  passwd varchar(100) DEFAULT NULL,
  type INT DEFAULT NULL,
  privileges INT DEFAULT NULL,
  creation_date timestamp DEFAULT NULL
);

CREATE INDEX creation_date_idx ON userdb(creation_date);

create user flask with encrypted password 'W78&@Tn5tit&';
grant all privileges on table userdb to flask;
grant usage, select on all sequences in schema public to flask;
