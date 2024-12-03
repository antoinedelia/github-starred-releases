# GitHub Starred Releases

Get the latest releases of your starred repositories.

## Context

I'm starring repositories so that I can get releases news when I go to my GitHub homepage. This allows me to keep being updated with newest released for repositories I follow.

BUT, sometimes, and for a reason I can't explain, GitHub sometimes does not show these information on my homepage. So there's no way for me to get new releases.

This little script intend to fix this by getting starred repositories, find their latest release, and display them if they were created in the past week.

## Prerequisites

Create a [GitHub Personal Access Token](https://github.com/settings/tokens?type=beta) (PAT) with fine-grained permission, with at least permission for "Read access to starring".

Once you have this token, create a `.env` file, and put it in there:

```conf
GITHUB_PAT=YOUR_GITHUB_TOKEN
```

## Usage

```sh
uv sync

uv run main.py
```

Outputs:

```
Found 264 repos
No releases found for repository: antoinedelia/cloud-optimist
...
No releases found for repository: antoinedelia/RedditOverflow
Found 26 releases
Repository: dgtlmoon/changedetection.io
Release Name: 0.48.01 Single release - Fixing Scheduler UI options
Published At: 2024-12-03T17:45:10Z
URL: https://github.com/dgtlmoon/changedetection.io/releases/tag/0.48.01
----------------------------------------
Repository: syncthing/syncthing
Release Name: v1.28.1
Published At: 2024-12-03T12:03:09Z
URL: https://github.com/syncthing/syncthing/releases/tag/v1.28.1
----------------------------------------
```