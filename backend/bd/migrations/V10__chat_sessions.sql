CREATE TABLE chat_sessions (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  token_hash       CHAR(64)    NOT NULL,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_activity_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at       TIMESTAMPTZ NOT NULL
);

CREATE TABLE chat_messages (
  id         BIGSERIAL PRIMARY KEY,
  session_id UUID        NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
  role       VARCHAR(10) NOT NULL CHECK (role IN ('user','assistant','system')),
  content    TEXT        NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_chat_messages_session ON chat_messages (session_id, id);
CREATE INDEX idx_chat_sessions_expires ON chat_sessions (expires_at);
