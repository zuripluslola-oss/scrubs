-- Must Love Scrubs — initial schema (Supabase / Postgres).
-- This mirrors web/prisma/schema.prisma. Use EITHER `npx prisma migrate deploy`
-- OR run this file in the Supabase SQL editor — not both. Identifiers match
-- Prisma's defaults so the app works with either route.

create type "Role" as enum ('STUDENT', 'INSTRUCTOR', 'ADMIN');

create table "User" (
  "id"        uuid primary key default gen_random_uuid(),
  "email"     text unique not null,
  "name"      text,
  "role"      "Role" not null default 'STUDENT',
  "createdAt" timestamptz not null default now()
);

create table "Question" (
  "id"         text primary key,
  "exam"       text not null,
  "cat"        text not null,
  "topic"      text,
  "difficulty" text not null,
  "level"      int not null default 3,
  "type"       text not null,
  "stem"       text not null,
  "free"       boolean not null default false,
  "opts"       jsonb,
  "correct"    jsonb,
  "cols"       jsonb,
  "rows"       jsonb,
  "condition"  jsonb,
  "actions"    jsonb,
  "parameters" jsonb,
  "tip"        text,
  "pearl"      text
);
create index on "Question" ("cat");
create index on "Question" ("type");

create table "Flashcard" (
  "id"         text primary key,
  "kind"       text not null default 'qa',
  "deck"       text not null,
  "topic"      text,
  "difficulty" int not null default 3,
  "front"      text not null,
  "back"       text,
  "rationale"  text,
  "hint"       text,
  "data"       jsonb
);
create index on "Flashcard" ("deck");

create table "drugs" (
  "id"        text primary key,
  "generic"   text not null,
  "brand"     text,
  "drugClass" text not null,
  "system"    text not null,
  "moa"       text not null,
  "uses"      jsonb not null,
  "dose"      text not null,
  "route"     text not null,
  "side"      jsonb not null,
  "adverse"   jsonb not null,
  "nursing"   jsonb not null,
  "labs"      jsonb not null,
  "contra"    jsonb not null,
  "teaching"  jsonb not null,
  "antidote"  text not null default 'None',
  "highalert" boolean not null default false,
  "prototype" boolean not null default false,
  "tip"       text,
  "pearl"     text
);
create index on "drugs" ("system");

create table "Attempt" (
  "id"         uuid primary key default gen_random_uuid(),
  "userId"     uuid not null references "User"("id"),
  "questionId" text not null references "Question"("id"),
  "correct"    boolean not null,
  "chosen"     jsonb,
  "timeMs"     int,
  "confidence" int,
  "sessionId"  text,
  "createdAt"  timestamptz not null default now()
);
create index on "Attempt" ("userId");
create index on "Attempt" ("questionId");

create table "ExamSession" (
  "id"        uuid primary key default gen_random_uuid(),
  "userId"    uuid not null references "User"("id"),
  "mode"      text not null,
  "startedAt" timestamptz not null default now(),
  "endedAt"   timestamptz,
  "ability"   double precision,
  "itemCount" int not null default 0,
  "score"     int,
  "verdict"   text,
  "meta"      jsonb
);
create index on "ExamSession" ("userId");

create table "Mastery" (
  "id"        uuid primary key default gen_random_uuid(),
  "userId"    uuid not null references "User"("id"),
  "topic"     text not null,
  "correct"   int not null default 0,
  "total"     int not null default 0,
  "level"     double precision not null default 3,
  "updatedAt" timestamptz not null default now(),
  unique ("userId", "topic")
);

create table "StudyPlan" (
  "id"        uuid primary key default gen_random_uuid(),
  "userId"    uuid not null references "User"("id"),
  "lengthMo"  int not null,
  "startDate" timestamptz not null,
  "done"      jsonb,
  "createdAt" timestamptz not null default now()
);
create index on "StudyPlan" ("userId");
