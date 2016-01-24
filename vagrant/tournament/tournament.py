#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error: Could not connect to database")


def deleteMatches():
    """Remove all the match records from the database."""
    db, c = connect()

    query = "DELETE FROM matches"
    c.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, c = connect()

    query = "DELETE FROM players"
    c.execute(query)
    db.commit()
    db.close()


def deleteTournamentPlayers(t_id):
    """Remove all the player records from the database.

    Args:
        t_id: Tournament ID (unique)

    """
    db, c = connect()

    query = "DELETE FROM players WHERE tournament = %s"
    c.execute(query, (t_id,))
    db.commit()
    db.close()


def deleteTournaments():
    """Remove all the tournament records from the database."""
    db, c = connect()

    query = "DELETE FROM tournaments"
    c.execute(query)
    db.commit()
    db.close()


def deleteTournament(t_id):
    """Remove specific tournament records from the database.

    Args:
        t_id: Tournament ID (unique)

    """
    db, c = connect()

    query = "DELETE FROM tournaments WHERE tournament = %s"
    c.execute(query, (t_id,))
    db.commit()
    db.close()


def deleteTournamentMatches(t_id):
    """Remove all the specific tournament matches records from the database.

    Args:
        t_id: Tournament ID (unique)

    """
    db, c = connect()

    query = "DELETE FROM matches WHERE tournament = %s"
    c.execute(query, (t_id,))
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, c = connect()

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
    db, c = connect()

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
    db, c = connect()

    query_player = "INSERT INTO players (name, tournament) VALUES(%s, %s)"
    c.execute(query_player, (name, t_id))

    db.commit()
    db.close()


def getTournamentPlayers(t_id):
    """ Get all players from a tournament, sorted by id.

    Args:
        t_id: tournament id (unique)
    """

    db, c = connect()
    query = "SELECT * FROM players WHERE tournament = %s"
    c.execute(query, (t_id,))
    players = c.fetchall()
    db.close()

    return players


def registerTournament(name):
    """Adds a tournament to the tournament database.

    The database assigns a unique serial id number for the tournament.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
        name: the tournament's name (need not be unique).

    Returns:
        id: tournament id (unique) for use in other functions
    """
    db, c = connect()

    query = "INSERT INTO tournaments (name) VALUES(%s) RETURNING id"
    c.execute(query, (name,))
    id = c.fetchone()[0]

    db.commit()
    db.close()

    return id


def playerStandings(t_id):
    """Returns a list of the players and their total wins, sorted by wins, in
    a specific tournament.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
        t_id: tournament id (unique).

    Returns:
      A list of tuples, each of which contains
        (id, name, wins, ties, matches, omw, byes):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: total wins
        ties: total ties
        matches: the number of matches the player has played
        omw: total points of opponents a player has faced
        byes: the number of skips rounds player has in case of uneven players
    """
    db, c = connect()

    query = """SELECT player, name, wins, ties, matches, omw, byes
               FROM player_standings WHERE tournament = %s
               ORDER BY wins DESC, ties DESC, omw DESC"""
    c.execute(query, (t_id,))
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

    db, c = connect()

    query_match = """INSERT INTO matches (tournament, winner, loser, draw)
                     VALUES (%s, %s, %s, %s)"""
    c.execute(query_match, (t_id, winner, loser, draw))

    db.commit()
    db.close()


def checkForEvenPlayers(players, t_id):
    """Returns an even number of players, assigning a bye to one of the players,
    if there was an odd number of players to begin with

    Args:
        players: a list of tuples containing (id, name) of the player
        t_id: tournament id

    Returns:
        A even list of tuples containing (id, name) of the player, excluding
        the player assigned the bye if the initial list length was an odd
    """

    if len(players) % 2 != 0:
        db, c = connect()

        # Get player standings and select 1st place player without a bye (id)
        query = """SELECT player FROM player_standings WHERE bye = 0
                   ORDER BY score DESC, matches DESC LIMIT 1"""
        c.execute(query)
        id = c.fetchone()[0]

        # Update player with (id) to have a bye
        query_bye = "UPDATE player_standings SET bye=1 WHERE player = %s"
        c.execute(query_bye, (id,))

        # Get List of players excluding player with (id)
        query_players = """SELECT ps.player, p.name
                           FROM player_standings AS ps, players AS p
                           WHERE ps.player != %s AND ps.player = p.id
                           AND ps.tournament = %s
                           ORDER BY score DESC, matches DESC"""
        c.execute(query_players, (id, t_id))
        players_modified = c.fetchall()

        db.commit()
        db.close()

        # Return modified players list of tuples (id, name)
        return players_modified
    else:
        return players


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

    db, c = connect()

    query = """SELECT ps.player, p.name
               FROM player_standings AS ps, players AS p
               WHERE ps.player = p.id AND ps.tournament = %s
               ORDER BY score DESC, matches DESC"""
    c.execute(query, (t_id,))
    players = c.fetchall()

    players = checkForEvenPlayers(players, t_id)

    pairings = []
    for i in range(0, len(players), 2):
        # Append a tuple (player1 id, player1 name, player2 id, player2 name)
        pairings.append(
            (players[i][0], players[i][1], players[i+1][0], players[i+1][1],)
        )

    db.close()

    return pairings
