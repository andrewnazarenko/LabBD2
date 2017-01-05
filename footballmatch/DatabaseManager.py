import MySQLdb as mdb
import json


class DB(object):
    def __init__(self):
        self.connection = None

    def connect(self):
        if self.connection is not None:
            return
        try:
            self.connection = mdb.connect('localhost', 'root', 'pass', 'MatchUp')

        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            self.connection = None

    def getMatchList(self):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "select MatchUp.match.id, MatchUp.match.date, MatchUp.match.res1, MatchUp.match.res2, "
            "MatchUp.stadium.name as stadium_name, "
            "MatchUp.stadium.adress, MatchUp.stadium.capacity, "
            "team1.name as team1_name, team1.city as team1_city, team1.coach as team1_coach, "
            "team2.name as team2_name, team2.city as team2_city, team2.coach as team2_coach "
            "from MatchUp.match, MatchUp.stadium, MatchUp.team as team1, "
            "MatchUp.team as team2 where "
            "MatchUp.match.stadium_id = MatchUp.stadium.id and MatchUp.match.team1_id = team1.id "
            "and MatchUp.match.team2_id = team2.id;")
        self.close()
        return cur.fetchall()

    def close(self):
        if self.connection is not None:
            self.connection.close()
        self.connection = None

    def initialization(self):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)

        cur.execute("DELETE FROM MatchUp.match")
        cur.execute("ALTER TABLE MatchUp.match AUTO_INCREMENT = 1")
        cur.execute("commit")

        cur.execute("DELETE FROM MatchUp.team")
        cur.execute("ALTER TABLE MatchUp.team AUTO_INCREMENT = 1")
        cur.execute("commit")

        cur.execute("DELETE FROM MatchUp.stadium")
        cur.execute("ALTER TABLE MatchUp.stadium AUTO_INCREMENT = 1")
        cur.execute("commit")

        with open('matches.json', 'rb') as data_file:
            data = json.load(data_file)
            for stadium in data["stadiums"]:
                cur.execute("INSERT INTO MatchUp.stadium (capacity, adress, name)"
                            " VALUES('%s', '%s', '%s')" %
                            (stadium["capacity"], stadium["adress"], stadium["name"]))
                cur.execute("commit")

            for team in data["teams"]:
                cur.execute("INSERT INTO MatchUp.team (city, coach, name)"
                            " VALUES('%s', '%s', '%s')" %
                            (team["city"], team["coach"], team["name"]))
                cur.execute("commit")

            for match in data["matches"]:
                cur.execute("INSERT INTO MatchUp.match (team1_id, team2_id, stadium_id, res1, res2, DATE)"
                            " VALUES('%s', '%s', '%s', '%s', '%s', '%s')" %
                            (match["team1_id"], match["team2_id"], match["stadium_id"], match["res1"], match["res2"],
                             match["date"]))
                cur.execute("commit")

        self.close()

    def getTeamList(self):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "select * FROM MatchUp.team;")
        self.close()
        return cur.fetchall()

    def getStadiumList(self):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "SELECT * FROM MatchUp.stadium;")
        self.close()
        return cur.fetchall()

    def saveMatch(self, team1id, team2id, stadiumid, score1, score2, datetime):
        self.connect()
        if self.connection is None:
            return []
        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute("INSERT INTO MatchUp.match (team1_id, team2_id, stadium_id, res1, res2, DATE)"
                    " VALUES('%s', '%s', '%s', '%s', '%s', '%s')" %
                    (int(team1id), int(team2id), int(stadiumid), int(score1), int(score2), datetime))
        cur.execute("commit")
        self.close()

    def removeMatch(self, id):
        self.connect()
        if self.connection is None:
            return []
        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute("DELETE FROM MatchUp.match WHERE id = '%d' " % (int(id)))
        cur.execute("commit")
        self.close()

    def getMatch(self, id):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "select MatchUp.match.id, MatchUp.match.date, MatchUp.match.res1, MatchUp.match.res2, "
            "MatchUp.stadium.name as stadium_name, MatchUp.stadium.id as stadium_id, "
            "MatchUp.stadium.adress, MatchUp.stadium.capacity, "
            "team1.id as team1_id, team1.name as team1_name, team1.city as team1_city, team1.coach as team1_coach, "
            "team2.id as team2_id, team2.name as team2_name, team2.city as team2_city, team2.coach as team2_coach "
            "from MatchUp.match, MatchUp.stadium, MatchUp.team as team1, "
            "MatchUp.team as team2 where "
            "MatchUp.match.stadium_id = MatchUp.stadium.id and MatchUp.match.team1_id = team1.id "
            "and MatchUp.match.team2_id = team2.id "
            "and MatchUp.match.id = '%d' " % (int(id)))
        self.close()
        return cur.fetchone()

    def editMatch(self, team1id, team2id, stadiumid, score1, score2, datetime, id):
        self.connect()
        if self.connection is None:
            return []
        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "UPDATE MatchUp.match SET team1_id = '%s', team2_id = '%s', stadium_id = '%s', res1 = '%s', res2 = '%s', DATE = '%s'"
            " WHERE id = '%d' " %
            (int(team1id), int(team2id), int(stadiumid), int(score1), int(score2), datetime, int(id)))
        cur.execute("commit")
        self.close()

    def searchDate(self, date1, date2):
        self.connect()
        if self.connection is None:
            return []
        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute("select MatchUp.match.id, MatchUp.match.date, MatchUp.match.res1, MatchUp.match.res2, "
                    "MatchUp.stadium.name as stadium_name, MatchUp.stadium.id as stadium_id, "
                    "MatchUp.stadium.adress, MatchUp.stadium.capacity, "
                    "team1.id as team1_id, team1.name as team1_name, team1.city as team1_city, team1.coach as team1_coach, "
                    "team2.id as team2_id, team2.name as team2_name, team2.city as team2_city, team2.coach as team2_coach "
                    "from MatchUp.match, MatchUp.stadium, MatchUp.team as team1, "
                    "MatchUp.team as team2 where "
                    "MatchUp.match.stadium_id = MatchUp.stadium.id and MatchUp.match.team1_id = team1.id "
                    "and MatchUp.match.team2_id = team2.id "
                    "and MatchUp.match.date between '%s' AND '%s' " % ((date1), (date2)))

        self.close()
        return cur.fetchall()

    def searchWin(self, res):
        self.connect()
        if self.connection is None:
            return []
        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute("select MatchUp.match.id, MatchUp.match.date, MatchUp.match.res1, MatchUp.match.res2, "
                    "MatchUp.stadium.name as stadium_name, MatchUp.stadium.id as stadium_id, "
                    "MatchUp.stadium.adress, MatchUp.stadium.capacity, "
                    "team1.id as team1_id, team1.name as team1_name, team1.city as team1_city, team1.coach as team1_coach, "
                    "team2.id as team2_id, team2.name as team2_name, team2.city as team2_city, team2.coach as team2_coach "
                    "from MatchUp.match, MatchUp.stadium, MatchUp.team as team1, "
                    "MatchUp.team as team2 where "
                    "MatchUp.match.stadium_id = MatchUp.stadium.id and MatchUp.match.team1_id = team1.id "
                    "and MatchUp.match.team2_id = team2.id "
                    "and (MatchUp.match.res1 " + res + " MatchUp.match.res2)")
        self.close()
        return cur.fetchall()

    def search(self, fullword, incword, exword):
        self.connect()
        if self.connection is None:
            return []
        resword = '\"' + fullword + '\"'
        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute("select MatchUp.match.id, MatchUp.match.date, MatchUp.match.res1, MatchUp.match.res2, "
                    "MatchUp.stadium.name as stadium_name, MatchUp.stadium.id as stadium_id, "
                    "MatchUp.stadium.adress, MatchUp.stadium.capacity, "
                    "team1.id as team1_id, team1.name as team1_name, team1.city as team1_city, team1.coach as team1_coach, "
                    "team2.id as team2_id, team2.name as team2_name, team2.city as team2_city, team2.coach as team2_coach "
                    "from MatchUp.match, MatchUp.stadium, MatchUp.team as team1, "
                    "MatchUp.team as team2 where "
                    "MatchUp.match.stadium_id = MatchUp.stadium.id and MatchUp.match.team1_id = team1.id "
                    "and MatchUp.match.team2_id = team2.id ")
        self.close()
        return cur.fetchall()
