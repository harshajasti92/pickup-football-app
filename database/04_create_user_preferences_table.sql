-- Create user_preferences table for Pickup Football App
-- This table stores user preferences for game discovery and notifications

CREATE TABLE IF NOT EXISTS user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    preferred_days TEXT[], -- ['monday', 'wednesday', 'friday']
    preferred_times TEXT[], -- ['morning', 'evening']
    max_travel_distance INTEGER DEFAULT 10, -- km
    notifications_enabled BOOLEAN DEFAULT true,
    auto_join_skill_range INTEGER[] DEFAULT '{-2, 2}', -- relative to user skill
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_user_preferences_preferred_days ON user_preferences USING GIN(preferred_days);
CREATE INDEX IF NOT EXISTS idx_user_preferences_preferred_times ON user_preferences USING GIN(preferred_times);
CREATE INDEX IF NOT EXISTS idx_user_preferences_notifications ON user_preferences(notifications_enabled);

-- Create trigger to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_user_preferences_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_preferences_updated_at 
    BEFORE UPDATE ON user_preferences 
    FOR EACH ROW 
    EXECUTE FUNCTION update_user_preferences_updated_at_column();

-- Add constraints and checks
ALTER TABLE user_preferences ADD CONSTRAINT IF NOT EXISTS check_max_travel_distance 
    CHECK (max_travel_distance >= 0 AND max_travel_distance <= 100);

ALTER TABLE user_preferences ADD CONSTRAINT IF NOT EXISTS check_preferred_days 
    CHECK (preferred_days <@ ARRAY['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']);

ALTER TABLE user_preferences ADD CONSTRAINT IF NOT EXISTS check_preferred_times 
    CHECK (preferred_times <@ ARRAY['morning', 'afternoon', 'evening']);

ALTER TABLE user_preferences ADD CONSTRAINT IF NOT EXISTS check_auto_join_skill_range 
    CHECK (array_length(auto_join_skill_range, 1) = 2 AND auto_join_skill_range[1] <= auto_join_skill_range[2]);

-- Add comments for documentation
COMMENT ON TABLE user_preferences IS 'User preferences for game discovery and notifications';
COMMENT ON COLUMN user_preferences.preferred_days IS 'Array of preferred days: monday, tuesday, wednesday, thursday, friday, saturday, sunday';
COMMENT ON COLUMN user_preferences.preferred_times IS 'Array of preferred times: morning, afternoon, evening';
COMMENT ON COLUMN user_preferences.max_travel_distance IS 'Maximum travel distance in kilometers';
COMMENT ON COLUMN user_preferences.notifications_enabled IS 'Whether user wants to receive notifications';
COMMENT ON COLUMN user_preferences.auto_join_skill_range IS 'Skill range relative to user skill for auto-join suggestions [min_offset, max_offset]';

-- Function to create default preferences for new users
CREATE OR REPLACE FUNCTION create_default_user_preferences()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_preferences (
        user_id, 
        preferred_days, 
        preferred_times, 
        max_travel_distance, 
        notifications_enabled, 
        auto_join_skill_range
    ) VALUES (
        NEW.id,
        ARRAY['tuesday', 'thursday', 'saturday'], -- Default: weekends and mid-week
        ARRAY['evening'], -- Default: evening games
        15, -- Default: 15km radius
        true, -- Default: notifications enabled
        ARRAY[-2, 2] -- Default: ±2 skill levels
    );
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically create preferences for new users
CREATE TRIGGER create_user_preferences_on_signup
    AFTER INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION create_default_user_preferences();

-- Sample data for development (uncomment if needed)
/*
-- Sample user preferences (requires users to exist first)
INSERT INTO user_preferences (user_id, preferred_days, preferred_times, max_travel_distance, notifications_enabled, auto_join_skill_range)
VALUES 
    (1, ARRAY['tuesday', 'thursday', 'saturday'], ARRAY['evening'], 15, true, ARRAY[-2, 2]),
    (2, ARRAY['monday', 'wednesday', 'friday'], ARRAY['morning', 'afternoon'], 10, true, ARRAY[-1, 3]);
*/
