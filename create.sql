CREATE TABLE cafe
(
   id             SERIAL PRIMARY KEY,
   domain         VARCHAR (100) NOT NULL,
   url            VARCHAR (100) NOT NULL UNIQUE,
   name           VARCHAR (100) NOT NULL,
   address        VARCHAR (200),
   phone          VARCHAR (50),
   monday         VARCHAR (50),
   tuesday        VARCHAR (50),
   wednesday      VARCHAR (50),
   thursday       VARCHAR (50),
   friday         VARCHAR (50),
   saturday       VARCHAR (50),
   sunday         VARCHAR (50),
   status         VARCHAR (50),
   update_time    TIMESTAMP WITHOUT TIME ZONE
);