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

-- View for OMW
--
-- Columns: player id from matches, sum of wins
--
-- Tips: Left Join matches and player wins table. Match matches table losers to
-- player winner table (subquery) winners and add their total wins.
CREATE VIEW player_omws AS
    SELECT m.winner AS player, COALESCE(SUM(pw.wins), 0) AS omw
    FROM matches as m LEFT JOIN
        -- Player Wins Table (Subquery)
        (SELECT winner AS player, COUNT(*) as wins
            FROM matches
            GROUP BY player) as pw
    ON m.loser = pw.player
    GROUP BY m.winner;

-- View for Player Standings
--
-- Columns: tournament, player(id), name, wins, ties, omw, matches
-- Order By: tournament, wins, ties, omw
--
-- Tips: Left Join players table to matches (Group by player id)
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
        (SELECT omw FROM player_omws WHERE player = p.id) as omw,
        (SELECT byes FROM players WHERE id = p.id) as byes        
    FROM players AS p LEFT JOIN matches AS m
    ON (p.id = m.winner OR p.id = m.loser)
    GROUP BY p.id
    ORDER BY wins DESC, ties DESC, omw DESC, matches DESC;
