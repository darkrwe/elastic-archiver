
CREATE TABLE IF NOT EXISTS "elasticserver" ("id" INTEGER NOT NULL PRIMARY KEY, "host" TEXT NOT NULL, "created_at" INTEGER NOT NULL, "is_registered" INTEGER NOT NULL, "region" TEXT NOT NULL DEFAULT "us-east-1");
CREATE UNIQUE INDEX "elasticserver_host" ON "elasticserver" ("host");