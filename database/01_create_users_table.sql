-- Create users table for Pickup Football App
-- This table stores user information including authentication and profile data

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    age_range VARCHAR(20) CHECK (age_range IN ('18-25', '26-35', '36-45', '46+')),
    
    -- Profile information
    bio TEXT,
    profile_photo_url VARCHAR(500),
    
    -- Playing information
    skill_level INTEGER CHECK (skill_level >= 1 AND skill_level <= 10) DEFAULT 5,
    preferred_position VARCHAR(50) CHECK (preferred_position IN ('Goalkeeper', 'Defender', 'Midfielder', 'Forward', 'Any')),
    playing_style VARCHAR(100) CHECK (playing_style IN ('Aggressive', 'Technical', 'Physical', 'Balanced', 'Creative', 'Defensive')),
    
    -- Account status
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    verification_token VARCHAR(255),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_skill_level ON users(skill_level);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_age_range ON users(age_range);
CREATE INDEX IF NOT EXISTS idx_users_preferred_position ON users(preferred_position);

-- Create a trigger to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_the_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_the_updated_at_column();

-- Add some comments for documentation
COMMENT ON TABLE users IS 'Main users table storing player information and authentication data';
COMMENT ON COLUMN users.age_range IS 'Player age range: 18-25, 26-35, 36-45, 46+';
COMMENT ON COLUMN users.skill_level IS 'Player skill level from 1 (beginner) to 10 (professional)';
COMMENT ON COLUMN users.preferred_position IS 'Players preferred position: Goalkeeper, Defender, Midfielder, Forward, Any';
COMMENT ON COLUMN users.playing_style IS 'Players playing style: Aggressive, Technical, Physical, Balanced, Creative, Defensive';
COMMENT ON COLUMN users.is_verified IS 'Whether the user has verified their account';
