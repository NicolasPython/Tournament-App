#! /usr/bin/env python3
# coding: utf-8

from tinydb import TinyDB

class ManagementDataBase:
    """
    This class contains all methodes for save data into DataBase.
    """

    def __init__(self):
        self.db = TinyDB('db_echec.json')
        self.tournaments_table = self.db.table('tournaments')
        self.players_table = self.db.table('players')

    def serialize_players(self, player):
        serialize_player = {"first_name": player.first_name,
                            "last_name": player.last_name,
                            "birth_date": player.birth_date,
                            "gender": player.gender,
                            "ranking": player.ranking,
                            "point": player.points}
        
        return serialize_player

    def serialize_tournament(self, tournament):
        instances_players = tournament.players
        instances_rounds = tournament.rounds 

        dicts_players = []
        dicts_rounds = []        
        # serialized players
        for player in instances_players:
            instance = self.serialize_players(player)
            dicts_players.append(instance)
        # serialized rounds
        for round in instances_rounds:
            matchs_list = []
            name = round.name
            start_date = round.start_date
            end_date = round.end_date
            instances_matchs = round.matchs

            # serialized matchs
            for match in instances_matchs:
                player_1 = match.player_1
                player_2 = match.player_2

                serialized_player_1 = self.serialize_players(player_1)

                serialized_player_2 = self.serialize_players(player_2)

                points_p1 = match.points_p1
                points_p2 = match.points_p2

                serialized_match = ([serialized_player_1, points_p1], [serialized_player_2, points_p2])

                instance_match = {"match": serialized_match,
                                "player_1": serialized_player_1,
                                "player_2": serialized_player_2,
                                "points_p1": points_p1,
                                "points_p2": points_p2}

                matchs_list.append(instance_match)

            instance_round = {"name": name, "start_date": start_date, "end_date": end_date, "matchs": matchs_list,}

            dicts_rounds.append(instance_round)

        return {"name": tournament.name, 
                "place": tournament.place,
                "nb_rounds": tournament.nb_rounds,
                "time_control": tournament.time_control,
                "description": tournament.description,
                "date": tournament.date,
                "players_tournament": dicts_players,
                "all_round": dicts_rounds}

    def save_players(self, player):
        serialize_player = self.serialize_players(player)
        self.players_table.insert(serialize_player)

    def save_tournament(self, tournament):
        serialize_tournament = self.serialize_tournament(tournament)
        self.tournaments_table.insert(serialize_tournament)