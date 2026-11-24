-- V11: Link guest chat_sessions to registered candidate accounts (SA-29)
-- Runs after V10__chat_sessions.sql and V2__users_and_applications.sql

ALTER TABLE chat_sessions
  ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  ADD COLUMN IF NOT EXISTS claimed_at TIMESTAMPTZ;

CREATE INDEX IF NOT EXISTS idx_chat_sessions_user ON chat_sessions (user_id);
