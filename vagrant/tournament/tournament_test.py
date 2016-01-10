#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *


def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    print "2. Player records can be deleted. Tournaments can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament = registerTournament("Fun League")
    registerPlayer("Chandra Nalaar", tournament)
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament = registerTournament("Fun League")
    registerPlayer("Markov Chaney", tournament)
    registerPlayer("Joe Malik", tournament)
    registerPlayer("Mao Tsu-hsi", tournament)
    registerPlayer("Atlanta Hope", tournament)
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testTournamentRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament_1 = registerTournament("Fun League")
    tournament_2 = registerTournament("Pro League")
    registerPlayer("Markov Chaney", tournament_1)
    registerPlayer("Joe Malik", tournament_1)
    registerPlayer("Mao Tsu-hsi", tournament_1)
    registerPlayer("Atlanta Hope", tournament_2)
    c = countTournamentPlayers(tournament_1)
    if c != 3:
        raise ValueError(
            "After registering three players, countTournamentPlayers should be 3.")
    deleteTournamentPlayerStandings(tournament_1)
    c = countTournamentPlayers(tournament_1)
    if c != 0:
        raise ValueError("After deleting, countTournmanentPlayers should return zero.")
    print "5a. Tournament Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament = registerTournament("Fun League")
    registerPlayer("Melpomene Murray", tournament)
    registerPlayer("Randy Schwartz", tournament)
    standings = playerStandings(tournament)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, score1, matches1), (id2, name2, score2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or score1 != 0 or score2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament = registerTournament("Fun League")
    registerPlayer("Bruno Walton", tournament)
    registerPlayer("Boots O'Neal", tournament)
    registerPlayer("Cathy Burton", tournament)
    registerPlayer("Diane Grant", tournament)
    standings = playerStandings(tournament)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournament, id1, id2)
    reportMatch(tournament, id3, id4)
    standings = playerStandings(tournament)
    for (i, n, s, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and s != 2:
            raise ValueError("Each match winner should have one win (Score of 2).")
        elif i in (id2, id4) and s != 0:
            raise ValueError("Each match loser should have zero wins (Score of 0).")
    print "7. After a match, players have updated standings."


def testReportTieMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament = registerTournament("Fun League")
    registerPlayer("Bruno Walton", tournament)
    registerPlayer("Boots O'Neal", tournament)
    registerPlayer("Cathy Burton", tournament)
    registerPlayer("Diane Grant", tournament)
    standings = playerStandings(tournament)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournament, id1, id2)
    reportMatch(tournament, id3, id4, True)
    standings = playerStandings(tournament)
    for (i, n, s, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i == id1 and s != 2:
            raise ValueError("Player one should have one win (Score of 2).")
        elif i == id2 and s != 0:
            raise ValueError("Player two should have zero wins (Score of 0).")
        if i in (id3, id4) and s != 1:
            raise ValueError("Each draw match player should a score of 1.")
    print "7a. After a match, and a tie match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament = registerTournament("Fun League")
    registerPlayer("Twilight Sparkle", tournament)
    registerPlayer("Fluttershy", tournament)
    registerPlayer("Applejack", tournament)
    registerPlayer("Pinkie Pie", tournament)
    standings = playerStandings(tournament)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournament, id1, id2)
    reportMatch(tournament, id3, id4)
    pairings = swissPairings(tournament)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testTournamentRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testReportTieMatches()
    testPairings()
    print "Success!  All tests pass!"
