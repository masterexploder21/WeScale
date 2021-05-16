# This file is responsible only for database access

from azure.cosmos import exceptions, CosmosClient, PartitionKey


class DataRepository:
    endpoint_address = ""
    private_access_key = ""
    azure_client = None
    database = None
    database_name = ""
    static_data_container_name = ""
    history_data_container_name = ""
    static_container = None
    history_container = None

    def __init__(self, endpoint_address, private_access_key, database_name, static_data_container_name,
                 history_data_container_name):
        if private_access_key is None:
            raise Exception("Environmental variable for database private key is not set!")

        self.endpoint_address = endpoint_address
        self.private_access_key = private_access_key
        self.database_name = database_name
        self.static_data_container_name = static_data_container_name
        self.history_data_container_name = history_data_container_name

        self.azure_client = CosmosClient(self.endpoint_address, self.private_access_key)
        self.database = self.azure_client.create_database_if_not_exists(id=self.database_name)

        self.static_container = self.database.create_container_if_not_exists(
            id=self.static_data_container_name,
            partition_key=PartitionKey(path="/id"),
            offer_throughput=400
        )

        # TODO: add second container
        # self.history_container = self.database.create_container_if_not_exists(
        #     id=self.history_data_container_name,
        #     partition_key=PartitionKey(path="/id"),
        #     offer_throughput=400
        # )

    def get_static_data(self):
        query = "SELECT * FROM c"

        items = list(self.static_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        return items
