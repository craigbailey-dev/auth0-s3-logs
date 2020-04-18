# auth0-s3-logs
Capture Auth0 events through AWS EventBridge and store as logs in S3, query-able by Athena

## Architecture

![enter image description here](https://d50daux61fgb.cloudfront.net/auth0-s3-log/solution-architecture.png)

An EventBridge event rule for a given event bus tracks Auth0 events. The event rule targets a Kinesis Firehose delivery stream that will put log files into an S3 bucket. A Lambda function is used by the delivery stream to transform the CloudWatch event payload into the log file format. After a log file is placed in the bucket, a Lambda function is run that creates a partition for the Glue table, if one does not exist.

## Log Format

 - **log_id** *(string)* - The id of the log event
 - **timestamp** *(string)* - The moment when the event occured
 - **connection** *(string)* - The connection name related to the event
 - **connection_id** *(string)* - The connection id related to the event
 - **client_id** *(string)* - The client id related to the event
 - **client_name** *(string)* - The name of the client related to the event
 - **ip** *(string)* - The IP address from where the request that caused the log entry originated
 - **user_id** *(string)* - The user id related to the event
 - **user_name** *(string)* - The user name related to the event
 - **description** *(string)* - The description of the event
 - **user_agent** *(string)* - The user agent that is related to the event
 - **type** *(string)* - One of the [possible event types](https://auth0.com/docs/logs#log-data-event-listing)
 - **strategy** *(string)* - The connection strategy related to the event
 - **strategy_type** *(string)* - The connection strategy type related to the event
 - **hostname** *(string)* - the hostname that is being used for the authentication flow
 - **details** *(string)* - A JSON string containing additional information about the event. The content in this JSON can be extracted in Athena queries using [Presto functions](https://prestodb.io/docs/0.172/functions/json.html).

## Log Partitions

All Glue tables are partitioned by the date and hour that the log arrives in S3. It is highly recommended that Athena queries on Glue database filter based on these paritions, as it will greatly reduce quety execution time and the amount of data processed by the query.


## Build and Deploy

To deploy the application, use the `cloudformation package` command from the AWS CLI. 
 
#### Example:

`aws cloudformation package --template templates/root.yaml --s3-bucket $S3_BUCKET --s3-prefix $S3_PREFIX --output-template template-export.yaml`