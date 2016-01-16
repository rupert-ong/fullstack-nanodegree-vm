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


def deleteTournament(t_id):
    """Remove specific tournament records from the database.

    Args:
        t_id: Tournament ID (unique)

    """
    db = connect()
    c = db.cursor()

    query = "DELETE FROM tournaments WHERE tournament = %s"
    c.execute(query, (t_id,))
    db.commit()
    db.close()


def deleteTournamentMatches(t_id):
    """Remove all the specific tournament matches records from the database.

    Args:
        t_id: Tournament ID (unique)

    """
    db = connect()
    c = db.cursor()

    query = "DELETE FROM matches WHERE tournament = %s"
    c.execute(query, (t_id,))
    db.commit()
    db.close()


def deleteTournamentPlayerStandings(t_id):
    """Remove all the specific tournament player standings records from the
    database.

    Args:
        t_id: Tournament ID (unique)

    """
    db = connect()
    c = db.cursor()

    query = "DELETE FROM player_standings WHERE tournament = %s"
    c.execute(query, (t_id,))
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


def countTournamentPlayers(t_id):
    """Returns the number of players currently registered in a specific
    tournament from player_standings table.

        Args:
            t_id: tournament id (unique)

    """
    db = connect()
    c = db.cursor()

    query = """SELECT COUNT(*) AS num FROM player_standings
               WHERE tournament = %s"""
    c.execute(query, (t_id,))
    count = c.fetchone()[0]
    db.close()

    return count


def registerPlayer(name, t_id):
    """Adds a player to the tournament database to a specific tournament.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
        name: the player's full name (need not be unique).
        t_id: tournament id (unique).
    """
    db = connect()
    c = db.cursor()

    query_player = "INSERT INTO players (name) VALUES(%s) RETURNING id"
    c.execute(query_player, (name,))

    player_id = c.fetchone()[0]
    query_player_standing = """INSERT INTO player_standings (tournament,
        player, score, matches) VALUES(%s, %s, %s, %s)"""
    c.execute(query_player_standing, (t_id, player_id, 0, 0,))

    db.commit()
    db.close()


def registerTournament(name):
    """Adds a tournament to the tournament database.

    The database assigns a unique serial id number for the tournament.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
        name: the tournament's name (need not be unique).

    Returns:
        id: tournament id (unique) for use in other functions
    """
    db = connect()
    c = db.cursor()

    query = "INSERT INTO tournaments (name) VALUES(%s) RETURNING id"
    c.execute(query, (name,))
    id = c.fetchone()[0]

    db.commit()
    db.close()

    return id


def playerStandings(t_id):
    """Returns a list of the players and their total score, sorted by score, in
    a specific tournament.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
        t_id: tournament id (unique).

    Returns:
      A list of tuples, each of which contains (id, name, score, matches, omw):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        score: total points for wins and draws (2 for wins, 1 for draws)
        matches: the number of matches the player has played
        omw: total points of opponents a player has faced
    """
    db = connect()
    c = db.cursor()

    query = """SELECT ps.player, p.name, ps.score, ps.matches,
                (SELECT COALESCE(SUM(ps2.score), 0)
                    FROM player_standings AS ps2
                    WHERE ps2.player IN (SELECT loser FROM matches
                        WHERE winner = ps.player AND tournament = %s)
                    OR ps2.player IN (SELECT winner FROM matches
                        WHERE loser = ps.player AND tournament = %s)
                ) AS omw
                FROM player_standings AS ps, players AS p
                WHERE ps.player = p.id AND ps.tournament = %s
                ORDER BY ps.score DESC, omw DESC, ps.matches DESC"""
    c.execute(query, (t_id, t_id, t_id))
    players = c.fetchall()
    db.close()

    return players


def reportMatch(t_id, winner, loser, draw=False):
    """Records the outcome of a single match between two players. Updates
    Player Standings.

    Args:
        t_id: the tournament id
        winner: the id number of the player who won
        loser: the id number of the player who lost
        draw: boolean of if match was a tie. Changes points allotted in match
    """

    db = connect()
    c = db.cursor()

    query_match = """INSERT INTO matches (tournament, winner, loser, draw)
                    VALUES (%s, %s, %s, %s)"""
    c.execute(query_match, (t_id, winner, loser, draw))

    if(draw is False):
        query_winner = """UPDATE player_standings SET score = score + 2,
                        matches = matches + 1
                        WHERE tournament = %s AND player = %s"""
        query_loser = """UPDATE player_standings SET matches = matches + 1
                        WHERE tournament = %s AND player = %s"""
        c.execute(query_winner, (t_id, winner))
        c.execute(query_loser, (t_id, loser))
    else:
        query_draw = """UPDATE player_standings SET score = score + 1,
                        matches = matches + 1
                        WHERE tournament = %s AND player = %s"""
        c.execute(query_draw, (t_id, winner))
        c.execute(query_draw, (t_id, loser))

    db.commit()
    db.close()


def swissPairings(t_id):
    """Returns a list of pairs of players for the next round of a match in a
    specific tournament.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
        t_id: the tournament id

    Returns:
        A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name
    """

    db = connect()
    c = db.cursor()

    query = """SELECT ps.player, p.name FROM player_standings AS ps, players AS p
            WHERE ps.player = p.id AND ps.tournament = %s
            ORDER BY score DESC, matches DESC"""
    c.execute(query, (t_id,))
    players = c.fetchall()

    pairings = []
    for i in range(0, len(players), 2):
        pairings.append((players[i][0], players[i][1], players[i+1][0], players[i+1][1],))

    db.close()

    return pairings
