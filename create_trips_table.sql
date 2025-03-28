-- Drop the existing table if it exists
DROP TABLE IF EXISTS trips;

-- Create trips table with proper JSONB columns
CREATE TABLE trips (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    preferences JSONB NOT NULL,
    approved_suggestions JSONB NOT NULL,
    itinerary TEXT NOT NULL,
    status TEXT DEFAULT 'active' NOT NULL
);

-- Create index on created_at
CREATE INDEX idx_trips_created_at ON trips(created_at DESC);

-- Enable RLS
ALTER TABLE trips ENABLE ROW LEVEL SECURITY;

-- Allow all operations (you can restrict this later)
CREATE POLICY "Allow all operations" ON trips
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Create a trigger to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc'::text, NOW());
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_trips_updated_at
    BEFORE UPDATE ON trips
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();