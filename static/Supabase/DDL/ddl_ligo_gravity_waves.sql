create table public.ligo_gravity_waves (
  id uuid not null default gen_random_uuid (),
  superevent_id text null,
  grace_id text null,
  created timestamp without time zone null,
  n_events smallint null,
  t_start double precision null,
  t_0 double precision null,
  t_end double precision null,
  t_dur double precision null,
  t_latency double precision null,
  far double precision null,
  likelihood double precision null,
  "group" text null,
  instruments text null,
  pipeline text null,
  inserted_at timestamp without time zone null default now(),
  total_count integer null
  constraint ligo_gcn_alerts_pkey primary key (id)
) TABLESPACE pg_default;
