"""
Issue Management System Example

This example demonstrates how to use the issue/feedback gathering system
to report and track issues related to extracurricular activities.
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def create_issue_example():
    """Example: Creating a new issue"""
    print("\n=== Creating a New Issue ===")
    
    issue_data = {
        "title": "Chess Club meeting room too small",
        "description": "The current meeting room can't accommodate all participants when we have tournaments. We need a larger space.",
        "category": "feedback",
        "related_activity": "Chess Club",
        "reporter_email": "john@mergington.edu"
    }
    
    response = requests.post(f"{BASE_URL}/issues", json=issue_data)
    
    if response.status_code == 200:
        issue = response.json()
        print(f"✓ Issue created successfully!")
        print(f"  Issue ID: {issue['id']}")
        print(f"  Title: {issue['title']}")
        print(f"  Status: {issue['status']}")
        print(f"  Created: {issue['created_at']}")
        return issue['id']
    else:
        print(f"✗ Failed to create issue: {response.json()}")
        return None


def list_issues_example():
    """Example: Listing all issues"""
    print("\n=== Listing All Issues ===")
    
    response = requests.get(f"{BASE_URL}/issues")
    
    if response.status_code == 200:
        issues = response.json()
        print(f"Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  #{issue['id']}: {issue['title']} [{issue['status']}]")
    else:
        print(f"✗ Failed to fetch issues: {response.json()}")


def filter_issues_example():
    """Example: Filtering issues by category"""
    print("\n=== Filtering Issues by Category ===")
    
    # Get only bug reports
    response = requests.get(f"{BASE_URL}/issues?category=bug")
    
    if response.status_code == 200:
        issues = response.json()
        print(f"Found {len(issues)} bug report(s):")
        for issue in issues:
            print(f"  #{issue['id']}: {issue['title']}")
    else:
        print(f"✗ Failed to fetch issues: {response.json()}")


def update_issue_status_example(issue_id):
    """Example: Updating issue status"""
    print("\n=== Updating Issue Status ===")
    
    response = requests.patch(
        f"{BASE_URL}/issues/{issue_id}/status?status=in_progress"
    )
    
    if response.status_code == 200:
        issue = response.json()
        print(f"✓ Issue #{issue_id} status updated to: {issue['status']}")
    else:
        print(f"✗ Failed to update issue: {response.json()}")


def get_issue_details_example(issue_id):
    """Example: Getting specific issue details"""
    print("\n=== Getting Issue Details ===")
    
    response = requests.get(f"{BASE_URL}/issues/{issue_id}")
    
    if response.status_code == 200:
        issue = response.json()
        print(f"Issue #{issue['id']}:")
        print(f"  Title: {issue['title']}")
        print(f"  Description: {issue['description']}")
        print(f"  Category: {issue['category']}")
        print(f"  Status: {issue['status']}")
        print(f"  Reporter: {issue['reporter_email']}")
        if issue['related_activity']:
            print(f"  Related Activity: {issue['related_activity']}")
    else:
        print(f"✗ Failed to fetch issue: {response.json()}")


def ai_analysis_example():
    """Example: Getting AI-powered issue analysis"""
    print("\n=== AI-Powered Issue Analysis ===")
    
    response = requests.get(f"{BASE_URL}/ai/issues-summary")
    
    if response.status_code == 200:
        analysis = response.json()
        print(f"Total Issues: {analysis['total_issues']}")
        print(f"\nAI Analysis:\n{analysis['ai_analysis']}")
    elif response.status_code == 503:
        print("ℹ AI features are not enabled (ANTHROPIC_API_KEY required)")
    else:
        print(f"✗ Failed to get analysis: {response.json()}")


def run_examples():
    """Run all examples"""
    print("=" * 60)
    print("Issue Management System Examples")
    print("=" * 60)
    print("\nMake sure the API server is running:")
    print("  cd src && python app.py")
    print()
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/activities")
        if response.status_code != 200:
            print("✗ API server is not responding correctly")
            return
        
        # Run examples
        issue_id = create_issue_example()
        
        # Create a few more issues for demonstration
        requests.post(f"{BASE_URL}/issues", json={
            "title": "Add more programming workshops",
            "description": "Would love advanced Python and web development courses",
            "category": "feature_request",
            "related_activity": "Programming Class",
            "reporter_email": "emma@mergington.edu"
        })
        
        requests.post(f"{BASE_URL}/issues", json={
            "title": "Signup button not working on mobile",
            "description": "Can't sign up for activities from my phone",
            "category": "bug",
            "reporter_email": "michael@mergington.edu"
        })
        
        list_issues_example()
        filter_issues_example()
        
        if issue_id:
            update_issue_status_example(issue_id)
            get_issue_details_example(issue_id)
        
        ai_analysis_example()
        
        print("\n" + "=" * 60)
        print("Examples completed successfully!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to API server")
        print("  Please make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    run_examples()
