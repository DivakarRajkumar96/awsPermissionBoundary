import boto3
import json
import os
import logging

PermissionsBoundary = 'arn:aws:iam::aws:policy/AWSPriceListServiceFullAccess'

def get_lambda_role(lambda_function_name, session, region):
    """
    Retrieve the IAM role associated with the Lambda function.
    """
    lambda_client = session.client('lambda', region_name=region)
    try:
        response = lambda_client.get_function(FunctionName=lambda_function_name)
        role_arn = response['Configuration']['Role']
        print(f"Lambda function role ARN: {role_arn}")
        return role_arn
    except Exception as err:
        print(f"Error retrieving Lambda function role: {err}")
        return None

def put_role_permissions_boundary(role_name, permissions_boundary, session):
    """
    Add a permissions boundary to the IAM role.
    """
    client = session.client('iam')
    try:
        client.put_role_permissions_boundary(RoleName=role_name, PermissionsBoundary=permissions_boundary)
        return True
    except Exception as err:
        print(f"Error applying permissions boundary: {err}")
        return False

def delete_role_permissions_boundary(role_name, session):
    """
    Remove the permissions boundary from the IAM role.
    """
    client = session.client('iam')
    try:
        client.delete_role_permissions_boundary(RoleName=role_name)
        return True
    except Exception as err:
        print(f"Error deleting permissions boundary: {err}")
        return False

def aws_iam_enforce(request):
    """
    Main function to enforce IAM permissions boundary based on Lambda function details.
    """
    request_json = request.get_json(silent=True)

    account_id = request_json.get('account')
    lambda_function_name = request_json.get('lambda_function_name')
    action = request_json.get('action')  # 'add' or 'remove'
    region = request_json.get('region', 'eu-west-2')  # Default to 'eu-west-2' if not provided

    if not account_id or not lambda_function_name or not action or action not in ['add', 'remove']:
        return {'error': 'Invalid request parameters'}, 400

    # Retrieve AWS credentials from environment variables
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_session_token = os.getenv("AWS_SESSION_TOKEN")  # Make sure the session token is available

    if not aws_access_key_id or not aws_secret_access_key:
        return {'error': 'AWS credentials are not set in environment variables'}, 400

    # Create session with all required credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,  # Only include this if you're using temporary credentials
        region_name=region
    )

    # Get the IAM role associated with the Lambda function
    role_arn = get_lambda_role(lambda_function_name, session, region)
    if not role_arn:
        return {'error': 'Unable to retrieve Lambda function role.'}, 400
    
    # Extract the role name from the ARN
    role_name = role_arn.split('/')[-1]  # Role name is the last part of ARN

    # Apply or remove permissions boundary
    if action == 'add':
        if put_role_permissions_boundary(role_name, PermissionsBoundary, session):
            return {'status': f'Permissions boundary added to role: {role_name}'}, 200
        else:
            return {'error': f'Failed to add permissions boundary to role: {role_name}'}, 500
    elif action == 'remove':
        if delete_role_permissions_boundary(role_name, session):
            return {'status': f'Permissions boundary removed from role: {role_name}'}, 200
        else:
            return {'error': f'Failed to remove permissions boundary from role: {role_name}'}, 500
