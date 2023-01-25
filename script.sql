CREATE DATABASE stella_manager_bot;

\c stella_manager_bot

CREATE TABLE listener(
    channel_id BIGINT NOT NULL,
    command_qualified_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (channel_id, command_qualified_name)
);
