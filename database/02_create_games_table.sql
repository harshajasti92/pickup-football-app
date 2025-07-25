-- Create games table for Pickup Football App
-- This table stores game information and details

-- psql -U postgres -d pickup_football -f 02_create_games_table.sql -- Run this command to create the table
-- psql -U postgres -d pickup_football -c "\dt" -- to check if the table was created successfully
-- psql -U postgres -d pickup_football -c "\d games" -- to describe the table structure

CREATE TABLE IF NOT EXISTS games (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    location VARCHAR(200) NOT NULL,
    date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_minutes INTEGER DEFAULT 90,
    max_players INTEGER DEFAULT 22,
    skill_level_min INTEGER DEFAULT 1,
    skill_level_max INTEGER DEFAULT 10,
    status VARCHAR(20) DEFAULT 'open', -- open, full, cancelled, completed
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_games_date_time ON games(date_time);
CREATE INDEX IF NOT EXISTS idx_games_status ON games(status);
CREATE INDEX IF NOT EXISTS idx_games_skill_range ON games(skill_level_min, skill_level_max);
CREATE INDEX IF NOT EXISTS idx_games_location ON games(location);
CREATE INDEX IF NOT EXISTS idx_games_created_by ON games(created_by);

-- Create trigger to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_games_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_games_updated_at 
    BEFORE UPDATE ON games 
    FOR EACH ROW 
    EXECUTE FUNCTION update_games_updated_at_column();

-- Add constraints and checks using DO block for compatibility
DO $$ 
BEGIN
    -- Add skill level range constraint
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'check_skill_level_range' 
        AND table_name = 'games'
    ) THEN
        ALTER TABLE games ADD CONSTRAINT check_skill_level_range 
            CHECK (skill_level_min >= 1 AND skill_level_max <= 10 AND skill_level_min <= skill_level_max);
    END IF;
    
    -- Add max players constraint
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'check_max_players' 
        AND table_name = 'games'
    ) THEN
        ALTER TABLE games ADD CONSTRAINT check_max_players 
            CHECK (max_players > 0 AND max_players <= 32);
    END IF;
    
    -- Add duration constraint
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'check_duration' 
        AND table_name = 'games'
    ) THEN
        ALTER TABLE games ADD CONSTRAINT check_duration 
            CHECK (duration_minutes > 0 AND duration_minutes <= 300);
    END IF;
    
    -- Add status constraint
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'check_status' 
        AND table_name = 'games'
    ) THEN
        ALTER TABLE games ADD CONSTRAINT check_status 
            CHECK (status IN ('open', 'full', 'cancelled', 'completed'));
    END IF;
END $$;

-- Add comments for documentation
COMMENT ON TABLE games IS 'Games table storing football game information and details';
COMMENT ON COLUMN games.status IS 'Game status: open (accepting players), full (max capacity), cancelled, completed';
COMMENT ON COLUMN games.skill_level_min IS 'Minimum skill level required (1-10)';
COMMENT ON COLUMN games.skill_level_max IS 'Maximum skill level allowed (1-10)';
COMMENT ON COLUMN games.duration_minutes IS 'Game duration in minutes (default 90)';
COMMENT ON COLUMN games.max_players IS 'Maximum number of players allowed';
COMMENT ON COLUMN games.created_by IS 'User ID who created this game';

-- Sample data for development (uncomment if needed)
/*
INSERT INTO games (title, description, location, date_time, max_players, skill_level_min, skill_level_max, created_by, status) 
VALUES 
    ('Friday Evening Football', 'Casual game for intermediate players', 'Central Park Field A', '2025-07-26 18:00:00+00:00', 20, 5, 8, 1, 'open'),
    ('Sunday Morning Match', 'Competitive game for skilled players', 'Riverside Courts', '2025-07-28 10:00:00+00:00', 16, 7, 10, 1, 'open'),
    ('Wednesday Pickup', 'All skill levels welcome', 'Downtown Sports Complex', '2025-07-30 19:00:00+00:00', 18, 1, 10, 1, 'open');
*/
