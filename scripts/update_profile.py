"""Generate a terminal-style GitHub profile. Python 3.12+, no dependencies."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import re
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def request_json(url):
    headers = {"User-Agent": "httpsGabbae-profile", "Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return json.load(response)


def fetch(username):
    user = request_json(f"https://api.github.com/users/{username}")
    repositories = []
    page = 1
    while True:
        batch = request_json(f"https://api.github.com/users/{username}/repos?type=owner&per_page=100&page={page}")
        repositories.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return {"user": user, "repositories": repositories}


def render(config, snapshot, dark):
    colors = ({"bg": "#161b22", "text": "#c9d1d9", "muted": "#7d8590", "line": "#30363d",
               "key": "#ffa657", "value": "#a5d6ff", "green": "#7ee787"} if dark else
              {"bg": "#f6f8fa", "text": "#24292f", "muted": "#57606a", "line": "#d0d7de",
               "key": "#953800", "value": "#0550ae", "green": "#116329"})
    user = snapshot["user"]
    repos = [r for r in snapshot["repositories"] if not r.get("private")]
    original = [r for r in repos if not r.get("fork")]
    languages = Counter(r["language"] for r in original if r.get("language"))
    top_language = languages.most_common(1)[0][0] if languages else "None yet"
    stars = sum(r.get("stargazers_count", 0) for r in original)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="1100" height="650" viewBox="0 0 1100 650" role="img" aria-labelledby="title desc">',
             f'<title id="title">{escape(config["name"])} | GitHub Profile</title>',
             '<desc id="desc">Terminal-style profile with an ASCII portrait of John Aldrin Doruca wearing sunglasses, a suit, and a tie, plus bio, contact details, and public GitHub statistics.</desc>',
             '<style>text { font-family: Consolas, "DejaVu Sans Mono", monospace; font-size: 15px; white-space: pre; } .small { font-size: 12px; } .portrait { font-size: 10px; }</style>',
             f'<rect width="1100" height="650" rx="15" fill="{colors["bg"]}"/>']

    def text(x, y, value, color="text", cls=""):
        parts.append(f'<text x="{x}" y="{y}" fill="{colors[color]}" class="{cls}">{escape(str(value))}</text>')

    def rule(y):
        parts.append(f'<path d="M32 {y}H1068" stroke="{colors["line"]}"/>')

    def row(y, key, value):
        # Reserve a fixed 18-character key column, with a generous value column.
        if len(key) > 17 or len(str(value)) > 48:
            raise ValueError(f"Profile row is too long: {key}: {value}")
        text(392, y, ".", "muted")
        text(412, y, key, "key")
        text(412 + len(key) * 9.04, y, " " + "." * max(1, 17 - len(key)) + " ", "muted")
        text(593, y, value, "value")

    text(32, 43, config["username"] + "@github", "green")
    text(275, 43, "~ / profile", "muted")
    text(1018, 43, "UTF-8", "muted", "small")
    rule(66)
    theme = "dark" if dark else "light"
    portrait = (ROOT / "art" / f"portrait-{theme}.txt").read_text(encoding="ascii").splitlines()
    if len(portrait) > 46 or any(len(line) > 60 for line in portrait):
        raise ValueError("ASCII portrait must fit within 60 columns and 46 rows")
    for i, line in enumerate(portrait):
        text(38, 126 + i * 8.6, line, "text", "portrait")
    text(65, 570, "B U I L D  /  L E A R N  /  R E P E A T", "key", "small")

    text(392, 110, config["name"])
    text(392, 132, "─" * 71, "muted")
    row(158, "Role", config["role"])
    row(182, "Focus", config["focus"])
    row(206, "Since", user["created_at"][:4] + " on GitHub")
    row(246, "Languages", config["languages"])
    row(270, "Database", config["database"])
    row(294, "Tools", config["tools"])
    row(334, "Interests", config["interests"])
    row(358, "Approach", config["approach"])
    text(392, 400, "- Contact " + "─" * 61)
    row(426, "GitHub", config["username"])
    row(450, "LinkedIn", config["linkedin"])
    text(392, 490, "- Public GitHub Stats " + "─" * 49)
    row(516, "Repositories", f'{user["public_repos"]:,} public / {len(original):,} original')
    row(540, "Stars / Followers", f'{stars:,} / {user["followers"]:,}')
    row(564, "Top language", top_language)
    rule(589)
    text(32, 618, "> keep building. keep learning._", "green")
    text(819, 618, datetime.now(timezone.utc).strftime("updated %Y-%m-%d UTC"), "muted", "small")
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, help="Use saved API data instead of the network")
    args = parser.parse_args()
    config = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
    username = config["username"]
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", username):
        raise ValueError("Invalid GitHub username")
    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8-sig")) if args.snapshot else fetch(username)
    if snapshot["user"]["login"].lower() != username.lower():
        raise ValueError("Snapshot does not belong to the configured GitHub user")
    # Render both before writing; failed requests or invalid config preserve existing assets.
    rendered = {"dark_mode.svg": render(config, snapshot, True),
                "light_mode.svg": render(config, snapshot, False)}
    for filename, svg in rendered.items():
        (ROOT / filename).write_text(svg, encoding="utf-8")
    print("Updated light and dark profile SVGs.")


if __name__ == "__main__":
    main()
