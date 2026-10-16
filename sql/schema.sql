-- Ejecuta este archivo completo en Supabase: SQL Editor -> New query -> Run

create extension if not exists vector;

-- Memoria de conversación
create table if not exists mensajes (
    id bigserial primary key,
    sesion_id text not null,
    rol text not null check (rol in ('user', 'assistant')),
    contenido text not null,
    tema text,
    dificultad text,
    uso_apuntes boolean,
    creado_en timestamptz not null default now()
);
create index if not exists mensajes_sesion_idx on mensajes (sesion_id, id);

-- Apuntes para RAG (embeddings de 1536 dimensiones: text-embedding-3-small)
create table if not exists apuntes (
    id bigserial primary key,
    archivo text not null,
    contenido text not null,
    embedding vector(1536)
);

-- Búsqueda por similitud (coseno)
create or replace function match_apuntes(
    query_embedding vector(1536),
    match_count int default 3,
    min_similarity float default 0.3
)
returns table (id bigint, archivo text, contenido text, similitud float)
language sql stable
as $$
    select a.id, a.archivo, a.contenido,
           1 - (a.embedding <=> query_embedding) as similitud
    from apuntes a
    where 1 - (a.embedding <=> query_embedding) > min_similarity
    order by a.embedding <=> query_embedding
    limit match_count;
$$;
