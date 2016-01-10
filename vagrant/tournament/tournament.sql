-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players ( id SERIAL PRIMARY KEY,
                       name TEXT );

CREATE TABLE tournaments (  id SERIAL PRIMARY KEY,
                            name TEXT );

CREATE TABLE matches (  id SERIAL PRIMARY KEY,
                        tournament INT,
                        winner INT,
                        loser INT,
                        draw BOOLEAN );

CREATE TABLE player_standings ( tournament INT,
                                player INT,
                                score INT,
                                matches INT );
