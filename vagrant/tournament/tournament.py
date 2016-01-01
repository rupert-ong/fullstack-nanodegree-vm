#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()

    query = "DELETE FROM matches"
    c.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()

    query = "DELETE FROM players"
    c.execute(query)
    db.commit()
    db.close()


def deleteTournaments():
    """Remove all the tournament records from the database."""
    db = connect()
    c = db.cursor()

    query = "DELETE FROM tournaments"
    c.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()

    query = "SELECT COUNT(*) AS num FROM players"
    c.execute(query)
    count = c.fetchone()[0]
    db.close()

    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
        name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()

    query_player = "INSERT INTO players (name) VALUES(%s) RETURNING id"
    c.execute(query_player, (name,))
    player_id = c.fetchone()[0]

    query_player_standing = "INSERT INTO player_standings (player, score, matches) VALUES(%s, %s, %s)"
    c.execute(query_player_standing, (player_id, 0, 0,))

    db.commit()
    db.close()


def registerTournament(name):
    """Adds a tournament to the tournament database.

    The database assigns a unique serial id number for the tournament.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
        name: the tournament's name (need not be unique).

    Returns:
        id: tournament id (unique) for use in other functions like
            registerPlayer and countPlayers
    """
    db = connect()
    c = db.cursor()

    query = "INSERT INTO tournaments (name) VALUES(%s) RETURNING id"
    c.execute(query, (name,))
    id = c.fetchone()[0]

    db.commit()
    db.close()

    return id


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()

    query = """SELECT ps.player, p.name, ps.score, ps.matches
                FROM player_standings AS ps, players AS p
                WHERE ps.player = p.id
                ORDER BY ps.score DESC, ps.matches DESC
            """
    c.execute(query)
    players = c.fetchall()
    db.close()

    return players


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
