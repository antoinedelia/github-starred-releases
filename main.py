import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GITHUB_PAT = os.getenv("GITHUB_PAT")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_PAT}",
    "X-GitHub-Api-Version": "2022-11-28",
}


def fetch_starred_repositories() -> list[dict]:
    """Fetch all repositories for a given user, handling pagination."""
    url = "https://api.github.com/user/starred"
    repositories = []

    while url:  # Continue while there are more pages
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.json().get('message')}")
            break

        # Add the current page of repositories to the list
        repositories.extend(response.json())

        # Get the 'Link' header to find the URL for the next page
        links = response.headers.get("Link")
        if links:
            next_link = None
            for link in links.split(","):
                if 'rel="next"' in link:
                    next_link = link.split(";")[0].strip(" <>")
            url = next_link
        else:
            url = None  # No more pages

    return repositories


def fetch_last_releases(repositories_urls: list[str]):
    """Fetch the last release for each repository and filter by date."""
    one_week_ago = datetime.now() - timedelta(weeks=1)
    recent_releases = []

    for repo_url in repositories_urls:
        repo_name = repo_url.replace("https://api.github.com/repos/", "")
        releases_url = f"{repo_url}/releases/latest"

        response = requests.get(releases_url, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            release_data = response.json()
            published_at = release_data.get("published_at")
            if published_at:
                # Parse published_at and check if it's within the last week
                published_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                if published_date > one_week_ago:
                    recent_releases.append(
                        {
                            "repository": repo_name,
                            "release_name": release_data.get("name"),
                            "published_at": published_at,
                            "url": release_data.get("html_url"),
                        }
                    )
        elif response.status_code == 404:
            # No releases found for this repository
            print(f"No releases found for repository: {repo_name}")
        else:
            print(f"Error fetching releases for {repo_name}: {response.status_code} - {response.json().get('message')}")

    return recent_releases


def main():
    repos = fetch_starred_repositories()
    repo_urls = [repo["url"] for repo in repos]
    print(f"Found {len(repo_urls)} repos")
    releases = fetch_last_releases(repo_urls)
    print(f"Found {len(releases)} releases")

    releases.sort(key=lambda release: release["published_at"], reverse=True)

    for release in releases:
        print(f"Repository: {release['repository']}")
        print(f"Release Name: {release['release_name']}")
        print(f"Published At: {release['published_at']}")
        print(f"URL: {release['url']}")
        print("-" * 40)


if __name__ == "__main__":
    main()
