#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *


def deleteAll():
    deleteMatches()
    deletePlayers()
    deleteTournaments()


def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteAll()
    print "2. Player records can be deleted. Tournaments can be deleted."


def testCount():
    deleteAll()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteAll()
    tournament = registerTournament("Fun League")
    registerPlayer("Chandra Nalaar", tournament)
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteAll()
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
    deleteAll()
    tournament_1 = registerTournament("Fun League")
    tournament_2 = registerTournament("Pro League")
    registerPlayer("Markov Chaney", tournament_1)
    registerPlayer("Joe Malik", tournament_1)
    registerPlayer("Mao Tsu-hsi", tournament_1)
    registerPlayer("Atlanta Hope", tournament_2)
    c = countTournamentPlayers(tournament_1)
    if c != 3:
        raise ValueError(
            "After registering three players, countTournamentPlayers "
            "should be 3.")
    deleteTournamentPlayers(tournament_1)
    c = countTournamentPlayers(tournament_1)
    if c != 0:
        raise ValueError("After deleting, countTournamentPlayers "
                         "should return zero.")
    print "5a. Tournament Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteAll()
    tournament = registerTournament("Fun League")
    registerPlayer("Melpomene Murray", tournament)
    registerPlayer("Randy Schwartz", tournament)
    standings = playerStandings(tournament)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 7:
        raise ValueError("Each playerStandings row should have seven columns "
                         "(including omw and byes).")
    [(id1, name1, wins1, ties1, matches1, omw1, bye1),
        (id2, name2, wins2, ties2, matches2, omw2, bye2)] = standings
    if (matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0 or
            ties1 != 0 or ties1 != 0):
        raise ValueError(
            "Newly registered players should have no matches, wins or ties.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteAll()
    tournament = registerTournament("Fun League")
    registerPlayer("Bruno Walton", tournament)
    registerPlayer("Boots O'Neal", tournament)
    registerPlayer("Cathy Burton", tournament)
    registerPlayer("Diane Grant", tournament)
    tournament_players = getTournamentPlayers(tournament)
    [id1, id2, id3, id4] = [row[0] for row in tournament_players]
    reportMatch(tournament, id1, id2)
    reportMatch(tournament, id3, id4)
    standings = playerStandings(tournament)
    for (i, n, w, t, m, o, b) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if t != 0:
            raise ValueError("No one should have a tie recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins.")
    print "7. After a match, players have updated standings."


def testReportTieMatches():
    deleteAll()
    tournament = registerTournament("Fun League")
    registerPlayer("Bruno Walton", tournament)
    registerPlayer("Boots O'Neal", tournament)
    registerPlayer("Cathy Burton", tournament)
    registerPlayer("Diane Grant", tournament)
    tournament_players = getTournamentPlayers(tournament)
    [id1, id2, id3, id4] = [row[0] for row in tournament_players]
    reportMatch(tournament, id1, id2)
    reportMatch(tournament, id3, id4, True)
    standings = playerStandings(tournament)
    for (i, n, w, t, m, o, b) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i == id1 and w != 1:
            raise ValueError("Player one should have one win.")
        elif i == id2 and w != 0:
            raise ValueError("Player two should have zero wins.")
        if i in (id3, id4) and t != 1:
            raise ValueError("Player three and four should have one tie each.")
    print "7a. After a match, and a tie match, players have updated standings."


def testPlayerStandingsOmw():
    deleteAll()
    tournament = registerTournament("Fun League")
    registerPlayer("Bruno Walton", tournament)
    registerPlayer("Boots O'Neal", tournament)
    registerPlayer("Cathy Burton", tournament)
    registerPlayer("Diane Grant", tournament)
    registerPlayer("Bob Hope", tournament)
    registerPlayer("Will Ferrell", tournament)
    registerPlayer("Kevin Hart", tournament)
    registerPlayer("Conan O'Brien", tournament)
    registerPlayer("Ice Cube", tournament)
    tournament_players = getTournamentPlayers(tournament)
    [
        id1, id2, id3, id4, id5, id6, id7, id8, id9
    ] = [row[0] for row in tournament_players]

    # Bruno Has 4 wins against easy players (2nd place)
    reportMatch(tournament, id1, id5)
    reportMatch(tournament, id1, id6)
    reportMatch(tournament, id1, id7)
    reportMatch(tournament, id1, id8)

    # Cathy has 1 win, making her a medium player (3rd place)
    reportMatch(tournament, id3, id9)

    # Boots 4 wins, 3 against easy, 1 against a medium player (1st place)
    reportMatch(tournament, id2, id5)
    reportMatch(tournament, id2, id6)
    reportMatch(tournament, id2, id7)
    reportMatch(tournament, id2, id3)

    standings = playerStandings(tournament)
    [
        (id1, name1, wins1, ties1, matches1, omw1, bye1),
        (id2, name2, wins2, ties2, matches2, omw2, bye2),
        (id3, name3, wins3, ties3, matches3, omw3, bye3)] = standings[0:3]

    if(
        set([name1, name2, name3]) !=
        set(["Boots O'Neal", "Bruno Walton", "Cathy Burton"])
    ):
        raise ValueError("Player with better OMW not listed in order")
    print "7b. Players with same scores listed in order by opponent match wins."


def testPairings():
    deleteAll()
    tournament = registerTournament("Fun League")
    registerPlayer("Twilight Sparkle", tournament)
    registerPlayer("Fluttershy", tournament)
    registerPlayer("Applejack", tournament)
    registerPlayer("Pinkie Pie", tournament)
    tournament_players = getTournamentPlayers(tournament)
    [id1, id2, id3, id4] = [row[0] for row in tournament_players]
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


def testBye():
    deleteAll()
    tournament = registerTournament("Fun League")
    registerPlayer("Twilight Sparkle", tournament)
    registerPlayer("Fluttershy", tournament)
    registerPlayer("Applejack", tournament)

    tournament_players = getTournamentPlayers(tournament)
    [id1, id2, id3] = [row[0] for row in tournament_players]

    # Fluttershy (now 1st, bye candidate) has a win against AppleJack (now 2nd)
    reportMatch(tournament, id2, id3)

    standings = playerStandings(tournament)

    players = checkForEvenPlayers(standings, tournament)
    [p_name1, p_name2] = [row[1] for row in players]

    standings = playerStandings(tournament)

    # 1st round: Check bye tallies
    for (i, n, w, t, m, o, b) in standings:
        if i == id2 and b != 1:
            raise ValueError("Player two bye should be 1.")
        if i in (id1, id3) and b != 0:
            raise ValueError("Player one and three should have 0 byes")

    if len(players) != 2:
        raise ValueError("Should have even players. Expecting 2, not 3.")
    elif "Fluttershy" in set([p_name1, p_name2]):
        raise ValueError("Player assigned bye should not in player list.")

    # 2nd round to test if previous bye player not byed again
    # (Should be Applejack this time as byed player)
    players = checkForEvenPlayers(standings, tournament)
    [p_name1, p_name2] = [row[1] for row in players]

    standings = playerStandings(tournament)

    # 2st round: Check bye tallies
    for (i, n, w, t, m, o, b) in standings:
        if i == id1 and b != 0:
            raise ValueError("Player one bye should be 0.")
        if i in (id2, id3) and b != 1:
            raise ValueError("Player two and three should have 1 byes")

    if len(players) != 2:
        raise ValueError("Should have even players. Expecting 2, not 3.")
    elif "Applejack" in set([p_name1, p_name2]):
        raise ValueError("Player assigned bye should not in player list.")
    print "8a. Only an even number of players are allowed in pairings."


def testPairingsAndBye():
    deleteAll()
    tournament = registerTournament("Fun League")
    registerPlayer("Twilight Sparkle", tournament)
    registerPlayer("Fluttershy", tournament)
    registerPlayer("Applejack", tournament)
    registerPlayer("Pinkie Pie", tournament)
    registerPlayer("Brain", tournament)
    tournament_players = getTournamentPlayers(tournament)
    [id1, id2, id3, id4, id5] = [row[0] for row in tournament_players]

    # Twilight Sparkle has most wins, should be byed player
    reportMatch(tournament, id1, id2)
    reportMatch(tournament, id1, id4)
    reportMatch(tournament, id3, id4)

    pairings = swissPairings(tournament)
    if len(pairings) != 2:
        raise ValueError(
            "For five players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings

    for (i1, n1, i2, n2) in pairings:
        if n1 == "Twilight Sparkle" or n2 == "Twilight Sparkle":
            raise ValueError("After one match, byed player should not be paired.")
            break

    print "8b. After one match, byed player excluded. Pairings are good."


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
    """
    testPlayerStandingsOmw()
    testPairings()
    testBye()
    testPairingsAndBye()"""
    print "Success!  All tests pass!"
