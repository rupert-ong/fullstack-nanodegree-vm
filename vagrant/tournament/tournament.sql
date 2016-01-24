-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE tournaments (  id SERIAL PRIMARY KEY,
                            name TEXT );

CREATE TABLE players ( id SERIAL PRIMARY KEY,
                       name TEXT,
                       tournament INTEGER REFERENCES tournaments(id),
                       byes INTEGER );

CREATE TABLE matches (  id SERIAL PRIMARY KEY,
                        tournament INTEGER REFERENCES tournaments(id),
                        winner INTEGER REFERENCES players(id),
                        loser INTEGER REFERENCES players(id),
                        draw BOOLEAN );

-- Create a View for Player Standing
--
-- Columns: tournament, player(id), name, wins, ties, omw, matches
-- Order By: tournament, wins, ties, omw
--
-- Tips: Left Join players table to matches

CREATE VIEW player_standings AS
    SELECT p.tournament, p.id AS player, p.name,
        (SELECT COUNT(*) 
            FROM matches
            WHERE winner = p.id AND draw = 'f') AS wins,
        (SELECT COUNT(*) 
            FROM matches
            WHERE (winner = p.id OR loser = p.id) AND draw = 't') AS ties,
        (SELECT COUNT(*) 
            FROM matches
            WHERE winner = p.id OR loser = p.id) AS matches,
        0 AS omw,
        (SELECT byes FROM players WHERE id = p.id) as byes        
    FROM players AS p LEFT JOIN matches AS m
    ON (p.id = m.winner OR p.id = m.loser)
    GROUP BY p.id
    ORDER BY wins DESC, ties DESC, omw DESC, matches DESC;
