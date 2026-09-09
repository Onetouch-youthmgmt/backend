-- Run this in Supabase SQL Editor right after creating a new user via
-- Authentication -> Users -> Add user (with an email + temporary password).
--
-- Sets:
--   1. their role (app_metadata, admin-only, not editable from the dashboard UI)
--   2. must_change_password = true (user_metadata) so the app forces them to
--      pick their own password the first time they sign in.
--
-- Replace the email and role ('admin' or 'karyakarta') below.

UPDATE auth.users
SET
  raw_app_meta_data = raw_app_meta_data || '{"role": "admin"}'::jsonb,
  raw_user_meta_data = raw_user_meta_data || '{"must_change_password": true}'::jsonb
WHERE email = 'someone@example.com';
