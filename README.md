# Swiss Pairing Tournament Results

**Swiss Pairing Tournament Results** is a database schema used to store game matches between players participating in multiple tournaments in the [Swiss Tournament Style](https://en.wikipedia.org/wiki/Swiss-system_tournament). This project is written in [Python](https://www.python.org) and [PostgreSQL](http://www.postgresql.org).

This is a project for the lovely folks at [Udacity](https://www.udacity.com), submitted for review by [Rupert Ong](http://twitter.com/rupertong), who is completing the Fullstack Web Developer Nanodegree.


## Table of contents

* [Quick start](#quick-start)
* [What's included](#whats-included)
* [Extra Credit](#extra-credit)
* [Contributors](#contributors)
* [Copyright and license](#copyright-and-license)


## Quick start

Here's what you need to do to view this project:

1. Install [Vagrant](https://www.vagrantup.com) and [VirtualBox](https://www.virtualbox.org).
2. Within Terminal (Mac), navigate to the vagrant folder and launch the Vagrant VM by running the command `vagrant up`.
3. SSH into the running Vagrant machine `vagrant ssh`. 
4. Execute `cd /vagrant/tournament` to change directory.
5. Execute `psql` and then create a database `CREATE DATABASE tournament;` and `\connect tournament` to connect to it.
6. Execute `\i tournament.sql` to import the database. `\quit` to exit PostgreSQL.
6. Execute `python tournament_test.py` to run the test suite.


### What's included

Within the downloaded files, this is the relevant structure:

```
fullstack-nanodegree-vm/
└── vagrant/
    ├── Vagrantfile
    └── pg_config.sh
    └── tournament/
        ├── tournament.py
        ├── tournament_test.py
        └── tournament.sql
```

## Extra Credit

1. If there is an odd number of players, assign one player a “bye” (skipped round). A bye counts as a free win. A player should not receive more than one bye in a tournament.
2. When two players have the same number of wins, rank them according to OMW (Opponent Match Wins), the total number of wins by players they have played against.
3. Support games where a draw (tied game) is possible.
4. Support more than one tournament in the database, so matches do not have to be deleted between tournaments.

## Contributors

**Rupert Ong**

* <https://twitter.com/rupertong>
* <https://github.com/rupert-ong>


## Copyright and license

Code and documentation copyright 2011-2016 Udacity Inc. All rights reserved.
