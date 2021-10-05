select count(*) from
(
    select
        u.first_name,
        u.last_name,
        u.email_address,
        u.user_id,
    from master.users u
)a
