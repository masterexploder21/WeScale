# This file is responsible only for database access
from azure.cosmos import CosmosClient, PartitionKey


class DataRepository:
    endpoint_address = ""
    private_access_key = ""
    azure_client = None
    database = None
    database_name = ""
    static_data_container_name = ""
    static_container = None

    def __init__(self, endpoint_address, private_access_key, database_name, static_data_container_name):
        if private_access_key is None:
            raise Exception("Environmental variable for database private key is not set!")

        self.endpoint_address = endpoint_address
        self.private_access_key = private_access_key
        self.database_name = database_name
        self.static_data_container_name = static_data_container_name

        self.azure_client = CosmosClient(self.endpoint_address, self.private_access_key)
        self.database = self.azure_client.create_database_if_not_exists(id=self.database_name)

        self.static_container = self.database.create_container_if_not_exists(
            id=self.static_data_container_name,
            partition_key=PartitionKey(path="/id"),
            offer_throughput=400
        )

    def execute_query(self, query):
        dictionary = next(self.static_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        dictionary.pop('id')
        stripped_dictionary = {}

        for item in dictionary:
            if not item.startswith('_'):
                stripped_dictionary[item] = dictionary[item]

        return stripped_dictionary

    def get_gold_chart_data(self, participant):
        query = "SELECT * FROM c WHERE c.id = \"gold_earned\""
        gold_data = self.execute_query(query)

        gold_data['YOU'] = participant.stats.gold_earned
        gold_earned = dict(sorted(gold_data.items(), key=lambda entry: entry[1]))
        gold_index = list(gold_earned.keys()).index('YOU')
        gold_max_value = round(int(list(gold_earned.values())[-1]) * 1.2, -3)
        gold_chart = {
            'name': 'gold_chart',
            'chart_values': list(gold_earned.values()),
            'chart_labels': list(gold_earned.keys()),
            'max_value': gold_max_value,
            'player_index': gold_index
        }

        return gold_chart

    def get_vs_chart_data(self, participant):
        query = "SELECT * FROM c WHERE c.id = \"vision_score\""
        vision_data = self.execute_query(query)

        vision_data['YOU'] = participant.stats.vision_score
        vision_scores = dict(sorted(vision_data.items(), key=lambda entry: entry[1]))
        vision_index = list(vision_scores.keys()).index('YOU')
        vision_max_value = round(int(list(vision_data.values())[-1]) * 1.2)
        vision_chart = {
            'name': 'vision_chart',
            'chart_values': list(vision_scores.values()),
            'chart_labels': list(vision_scores.keys()),
            'max_value': vision_max_value,
            'player_index': vision_index
        }

        return vision_chart

    def get_objectives_chart_data(self, participant):
        query = "SELECT * FROM c WHERE c.id = \"objectives_damage\""
        objectives_data = self.execute_query(query)

        objectives_data['YOU'] = participant.stats.damage_dealt_to_objectives
        objectives_scores = dict(sorted(objectives_data.items(), key=lambda entry: entry[1]))
        objectives_index = list(objectives_scores.keys()).index('YOU')
        objectives_max_value = round(int(list(objectives_scores.values())[-1]) * 1.2, -3)
        objectives_chart = {
            'name': 'objectives_chart',
            'chart_values': list(objectives_scores.values()),
            'chart_labels': list(objectives_scores.keys()),
            'max_value': objectives_max_value,
            'player_index': objectives_index
        }

        return objectives_chart


