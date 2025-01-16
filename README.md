# AWS IAM Permissions Boundary Enforcer for Lambda Functions

## Overview

This script allows you to enforce a permissions boundary on an IAM role associated with an AWS Lambda function. It supports two actions:

1. **Add** a permissions boundary to the IAM role.
2. **Remove** a permissions boundary from the IAM role.

This script leverages AWS SDK for Python (Boto3) and interacts with AWS Lambda and IAM services.

## Prerequisites

Before you can run this script, ensure that you have the following prerequisites:

### AWS Access

- **AWS Access Key and Secret Key**: You need to have valid AWS credentials set up. This script relies on environment variables for the AWS credentials:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_SESSION_TOKEN` (if you're using temporary credentials)

### IAM Permissions

The IAM role or user running this script must have the following permissions:

- **Lambda**: 
  - `lambda:GetFunction` — To retrieve the IAM role associated with the Lambda function.
  
- **IAM**:
  - `iam:PutRolePermissionsBoundary` — To apply a permissions boundary to an IAM role.
  - `iam:DeleteRolePermissionsBoundary` — To remove the permissions boundary from an IAM role.
  - `iam:GetRole` — To retrieve the role associated with the function.

Additionally, ensure that the IAM role you're applying the permissions boundary to has a valid permissions boundary ARN (the one defined in the script, i.e., `arn:aws:iam::aws:policy/AWSPriceListServiceFullAccess`).

### Dependencies

- **Python 3.x** (preferably Python 3.7 or higher)
- **Boto3** (AWS SDK for Python)

To install the required Python libraries, run:

```bash
pip install boto3
```

## Usage

1. Clone this repository to your local machine or cloud environment.

```bash
git clone https://github.com/your-repository/aws-iam-lambda-permissions-boundary.git
cd aws-iam-lambda-permissions-boundary
```

2. Set up your AWS credentials in environment variables:
```bash
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token  # if using temporary credentials
```

3. Run the script with the necessary JSON payload. You can pass this JSON payload using an HTTP POST request or directly within your environment if running locally.

## JSON Payload Structure

The script requires a JSON payload with the following fields:

```json
{
  "account": "<accountID>",
  "lambda_function_name": "<FunctionName>",
  "action": "<action>",  # "add" or "remove"
  "region": "<region>"   # e.g., "us-west-2", "eu-west-2"
}
```

## Example Request
```bash
curl -X POST https://your-api-endpoint.amazonaws.com \
  -H "Content-Type: application/json" \
  -d '{
    "account": "123456789012",
    "lambda_function_name": "MyLambdaFunction",
    "action": "add",
    "region": "us-west-2"
  }'
```

## Cloud Shell Testing (Google Cloud Shell)
To test this script from Google Cloud Shell using AWS CLI (assuming you have set up your AWS credentials):

1. Set your AWS credentials in the environment:
```bash
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token  # if using temporary credentials
```

2. Prepare the JSON payload and execute the request using AWS CLI. Example of payload to use:
```json
{
  "account": "<accountID>",
  "lambda_function_name": "<FunctionName>",
  "action": "<action>",  # 'add' or 'remove'
  "region": "<region>"   # Optional, default is 'eu-west-2'
}
```

3. You can execute this in Google Cloud Shell by running a simple curl request or by interacting with the API using requests or similar libraries from a Python script.
```bash
curl -X POST https://your-api-endpoint.amazonaws.com \
  -H "Content-Type: application/json" \
  -d '{
    "account": "123456789012",
    "lambda_function_name": "MyLambdaFunction",
    "action": "add",
    "region": "us-west-2"
  }'
```


## Response
The response will be either a success or error message:

Success:
```json
{
  "status": "Permissions boundary added to role: <role-name>"
}
```

Error:
```json
{
  "error": "Unable to retrieve Lambda function role."
}
```

## Example Usage
Assuming you want to add a permissions boundary to the Lambda function "MyLambdaFunction" in the "us-west-2" region for the account "123456789012", the JSON payload would look like:

```json
{
  "account": "123456789012",
  "lambda_function_name": "MyLambdaFunction",
  "action": "add",
  "region": "us-west-2"
}
```
Send this payload to the endpoint, and the script will add the specified permissions boundary to the IAM role associated with the Lambda function.
