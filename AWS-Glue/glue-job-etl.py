import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, year
from awsglue.context import GlueContext
from awsglue.transforms import ApplyMapping
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from awsglue.dynamicframe import DynamicFrame

# Get job arguments (fixing the NameError)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize Glue session
spark = SparkSession.builder.appName("NBAShotsCleaning").getOrCreate()
glueContext = GlueContext(spark)
job = Job(glueContext)
job.init(args["JOB_NAME"], args)  

# Load data from Glue Data Catalog
dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database="<Your-Glue-DB-Name>",  # Change to your actual database name
    table_name="<Your-Glue-Table-Name>"     # Change to your actual table name
)

# Convert to DataFrame
df = dynamic_frame.toDF()

# Convert GAME_DATE to Date format and extract year
df = df.withColumn("GAME_DATE", to_date(col("GAME_DATE"), "M-d-yyyy"))
df = df.withColumn("YEAR", year(col("GAME_DATE")))

# Cast the shot_distance column to DOUBLE and season_2 to INT
df = df.withColumn("SHOT_DISTANCE", col("SHOT_DISTANCE").cast("double"))
df = df.withColumn("SEASON_2", col("SEASON_2").cast("int"))

# Select relevant columns
df_cleaned = df.select(
    "YEAR", "SEASON_1", "SEASON_2", "TEAM_ID", "PLAYER_ID",
    "GAME_DATE", "GAME_ID", "EVENT_TYPE", "SHOT_MADE",
    "ACTION_TYPE", "SHOT_TYPE", "BASIC_ZONE", "ZONE_NAME",
    "ZONE_ABB", "ZONE_RANGE", "LOC_X", "LOC_Y",
    "SHOT_DISTANCE", "QUARTER", "MINS_LEFT", "SECS_LEFT"
)

# Convert back to DynamicFrame
dynamic_frame_cleaned = DynamicFrame.fromDF(df_cleaned, glueContext)

# Write cleaned data back to S3, overwrite existing data
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame_cleaned,
    connection_type="s3",
    connection_options={"path": "<Your-S3-Output-Bucket-ARN>"},
    format="parquet",
    format_options={"compression": "SNAPPY"}  # Optional compression option
)

# Commit job
job.commit()
