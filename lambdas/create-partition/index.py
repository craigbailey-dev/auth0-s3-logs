import boto3
import os
import traceback

# Initialize Glue client
glue_client = boto3.client("glue")

def handler(event, context):
    for record in event["Records"]:
        source_bucket = record["s3"]["bucket"]["name"]
        source_key = record["s3"]["object"]["key"]

        # Extract partition info from S3 key 
        folder, year, month, day, hour, _ = source_key.split("/")

        # Form date for 'date' partition column
        date = "{}-{}-{}".format(year, month, day)

        # Form S3 location for partition
        s3_location = 's3://{}/{}/{}/{}/{}'.format(source_bucket, folder, year, month, day, hour)

        # Form the partition input
        partition = {
            'Values': [
                date,
                hour
            ],
            "StorageDescriptor": {
                "NumberOfBuckets" : -1,
                "Columns": [
                    {
                        "Name": "log_id",
                        "Type": "string"
                    },
                    {
                        "Name": "timestamp",
                        "Type": "string"
                    },
                    {
                        "Name": "connection",
                        "Type": "string"
                    },
                    {
                        "Name": "connection_id",
                        "Type": "string"
                    },
                    {
                        "Name": "client_id",
                        "Type": "string"
                    },
                    {
                        "Name": "ip",
                        "Type": "string"
                    },
                    {
                        "Name": "user_id",
                        "Type": "string"
                    },
                    {
                        "Name": "user_name",
                        "Type": "string"
                    },
                    {
                        "Name": "description",
                        "Type": "string"
                    },
                    {
                        "Name": "user_agent",
                        "Type": "string"
                    },
                    {
                        "Name": "type",
                        "Type": "string"
                    },
                    {
                        "Name": "strategy",
                        "Type": "string"
                    },
                    {
                        "Name": "strategy_type",
                        "Type": "string"
                    },
                    {
                        "Name": "hostname",
                        "Type": "string"
                    },
                    {
                        "Name": "details",
                        "Type": "string"
                    }
                ],
                "Location": s3_location,
                "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                "Compressed": False,
                "SerdeInfo": {
                    "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe",
                    "Parameters": {
                        "serialization.format": "1"
                    }
                },
                "BucketColumns": [],
                "SortColumns": [],
                "Parameters": {},
                "SkewedInfo": {
                    "SkewedColumnNames": [],
                    "SkewedColumnValues": [],
                    "SkewedColumnValueLocationMaps": {}
                },
                "StoredAsSubDirectories": False
            }
        }

        # Attempt to create partition; Print exception if partition already exists or for any other error
        try:
            glue_client.create_partition(DatabaseName=os.environ["DATABASE_NAME"], TableName=os.environ["TABLE_NAME"], PartitionInput=partition)
        except:
            traceback.print_exc()