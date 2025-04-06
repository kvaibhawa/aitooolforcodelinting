import boto3
import time

# Initialize CodeGuru Reviewer client
client = boto3.client('codeguru-reviewer')

# Function to create a code review
def create_code_review(repository_name, source_code):
    try:
        response = client.create_code_review(
            Name="MyPythonCodeReview",
            RepositoryAssociationArn=f"arn:aws:codeguru-reviewer:{your_region}:{your_account_id}:repository-association/{repository_name}",
            SourceCodeType={
                'CodeCommit': {
                    'RepositoryName': repository_name,
                    'BranchName': 'main'
                }
            }
        )
        print("Code review creation initiated")
        return response['CodeReview']['CodeReviewArn']
    
    except Exception as e:
        print(f"Error creating code review: {e}")
        return None


# Function to check review status
def check_review_status(code_review_arn):
    try:
        response = client.describe_code_review(
            CodeReviewArn=code_review_arn
        )
        review_status = response['CodeReview']['Status']
        return review_status
    except Exception as e:
        print(f"Error checking review status: {e}")
        return None


def main():
    # Specify your repository and the code file you want to lint
    repository_name = "my-repository"
    source_code = "my_python_file.py"  # Assuming the Python code is in a repo

    # Step 1: Create a code review request
    code_review_arn = create_code_review(repository_name, source_code)
    
    if code_review_arn:
        # Step 2: Poll for the result of the review
        while True:
            status = check_review_status(code_review_arn)
            if status in ['Completed', 'Failed']:
                print(f"Code review completed with status: {status}")
                break
            print("Waiting for review to complete...")
            time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    main()
