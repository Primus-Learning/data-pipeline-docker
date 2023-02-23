import pandas as pd
import boto3
from io import BytesIO
from datetime import datetime

# Generate sample data
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'] * 20000,
    'age': [25, 32, 18, 41, 29] * 20000,
    'gender': ['F', 'M', 'F', 'M', 'F'] * 20000
}
df = pd.DataFrame(data)

# Convert dataframe to parquet format
buffer = BytesIO()
df.to_parquet(buffer)
buffer.seek(0)

# Get current date and timestamp
now = datetime.now()
date = now.strftime('%Y-%m-%d')
timestamp = now.strftime('%Y%m%d%H%M%S')

# Upload to S3 with partitions
s3 = boto3.resource('s3')
bucket_name = 'primlearning'
folder_name = f'upload_date={date}/upload_time={timestamp}'
key = f'{folder_name}/example.parquet'
s3.Object(bucket_name, key).put(Body=buffer)
