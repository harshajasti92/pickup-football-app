-- Create game_participants table for Pickup Football App
-- This table tracks user participation in games (junction table)

CREATE TABLE IF NOT EXISTS game_participants (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'confirmed', -- confirmed, waitlisted, declined
    position_preference VARCHAR(50),
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(game_id, user_id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_game_participants_game_id ON game_participants(game_id);
CREATE INDEX IF NOT EXISTS idx_game_participants_user_id ON game_participants(user_id);
CREATE INDEX IF NOT EXISTS idx_game_participants_status ON game_participants(status);
CREATE INDEX IF NOT EXISTS idx_game_participants_joined_at ON game_participants(joined_at);

-- Add constraints and checks
ALTER TABLE game_participants ADD CONSTRAINT IF NOT EXISTS check_participant_status 
    CHECK (status IN ('confirmed', 'waitlisted', 'declined'));

ALTER TABLE game_participants ADD CONSTRAINT IF NOT EXISTS check_position_preference 
    CHECK (position_preference IN ('Goalkeeper', 'Defender', 'Midfielder', 'Forward', 'Any') OR position_preference IS NULL);

-- Add comments for documentation
COMMENT ON TABLE game_participants IS 'Junction table tracking user participation in games';
COMMENT ON COLUMN game_participants.status IS 'Participation status: confirmed (playing), waitlisted (waiting), declined';
COMMENT ON COLUMN game_participants.position_preference IS 'Preferred position for this specific game';
COMMENT ON COLUMN game_participants.joined_at IS 'When the user joined this game';

-- Create function to automatically manage waitlist positions
CREATE OR REPLACE FUNCTION manage_waitlist_positions()
RETURNS TRIGGER AS $$
BEGIN
    -- When a confirmed player leaves, promote the first waitlisted player
    IF TG_OP = 'DELETE' AND OLD.status = 'confirmed' THEN
        UPDATE game_participants 
        SET status = 'confirmed'
        WHERE game_id = OLD.game_id 
        AND status = 'waitlisted'
        AND id = (
            SELECT id FROM game_participants 
            WHERE game_id = OLD.game_id AND status = 'waitlisted'
            ORDER BY joined_at ASC 
            LIMIT 1
        );
    END IF;
    
    RETURN COALESCE(NEW, OLD);
END;
$$ language 'plpgsql';

-- Create trigger for waitlist management
CREATE TRIGGER manage_waitlist_on_participant_change
    AFTER DELETE OR UPDATE ON game_participants
    FOR EACH ROW
    EXECUTE FUNCTION manage_waitlist_positions();

-- Sample data for development (uncomment if needed)
/*
-- Sample participants (requires games and users to exist first)
INSERT INTO game_participants (game_id, user_id, status, position_preference) 
VALUES 
    (1, 1, 'confirmed', 'Midfielder'),
    (1, 2, 'confirmed', 'Forward'),
    (2, 1, 'waitlisted', 'Defender'),
    (3, 2, 'confirmed', 'Any');
*/
