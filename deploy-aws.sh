export AWS_ACCESS_KEY_ID=mock_key
export AWS_SECRET_ACCESS_KEY=mock_secret
export AWS_DEFAULT_REGION=us-east-1

# Verify local emulator container engine status
aws s3 mb s3://employee-assets-bucket --endpoint-url=http://localhost:4566

# Build and run your Docker container pointing to your relational layer
docker build -t employee-app .
docker run -d -p 7000:7000 -e DATABASE_CONNECTION_STRING="Driver={ODBC Driver 17 for SQL Server};Server=host.docker.internal;Database=db_employee;UID=sa;PWD=YourSecurePassword;" employee-app