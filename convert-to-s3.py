import boto3
import pyarrow.parquet as pq
import pandas as pd
import pyarrow as pa

# AWS credentials
access_key_id = 'AKIAT7U2H26L2WRXB67L'
secret_access_key = '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'

# S3 bucket details
input_bucket_name = 'primlearning'
output_bucket_name = 'primuslearning-output'
output_prefix = 'output_date='

# Connect to S3
s3 = boto3.client('s3', aws_access_key_id=access_key_id,
                  aws_secret_access_key=secret_access_key)

# Get a list of all objects in the input bucket
response = s3.list_objects_v2(Bucket=input_bucket_name, Prefix='upload_date=')

# Loop over the objects and convert each one to CSV
for obj in response['Contents']:
    # Get the object key
    obj_key = obj['Key']

    # Load the Parquet file into memory
    print(f"Loading Parquet file from s3://{input_bucket_name}/{obj_key}")
    parquet_obj = s3.get_object(Bucket=input_bucket_name, Key=obj_key)
    parquet_bytes = parquet_obj['Body'].read()
    parquet_buf = pa.BufferReader(parquet_bytes)

    # Convert the Parquet file to a Pandas DataFrame
    table = pq.read_table(parquet_buf)
    df = table.to_pandas()

    # Convert the DataFrame to CSV
    csv_bytes = df.to_csv(index=False).encode('utf-8')

    # Upload the CSV file to S3
    output_key = f"{output_prefix}{obj_key.split('=')[1]}-{obj_key.split('=')[2].split('/')[0]}.csv"
    print(f"Uploading CSV file to s3://{output_bucket_name}/{output_key}")
    s3.put_object(Bucket=output_bucket_name, Key=output_key, Body=csv_bytes)

    # Delete the Parquet file from the input bucket
    print(f"Deleting Parquet file s3://{input_bucket_name}/{obj_key}")
    s3.delete_object(Bucket=input_bucket_name, Key=obj_key)

print("Done!")

