DROP TABLE IF EXISTS "slave";
DROP TABLE IF EXISTS "system";
DROP TABLE IF EXISTS "log";

CREATE TABLE "slave" (
  "uid" text NOT NULL,
  "mac" TEXT NOT NULL,
  "device_name" TEXT,
  "product_name" TEXT,
  "product_price" text,
  "device_frame" TEXT,
  "status_code" TEXT,
  PRIMARY KEY ("uid")
);

CREATE TABLE "system" (
  "login_name" TEXT,
  "login_pwd" TEXT NOT NULL
);

CREATE TABLE "log" (
  "uid" TEXT,
  "created" TEXT,
  "data" TEXT,
  CONSTRAINT PK_log PRIMARY KEY (uid)
);

INSERT into system(login_name, login_pwd) VALUES('bluetag', '6ae4feb835354ecf0b315ee701a41d14978d35e8392234ba4bdb01b085d47f68');
