# Install your GitHub profile

1. Open https://github.com/httpsGabbae/httpsGabbae and choose **Add file → Upload files**.
2. Upload the contents of this folder into the repository root on `main`. Replace the existing `README.md`. Include `dark_mode.svg`, `light_mode.svg`, `profile.json`, the `art/` and `scripts/` folders, and `.github/workflows/update-profile.yml`, preserving the folders. Commit the changes.
3. Open **Actions → Update profile → Run workflow** to check the first refresh. The workflow also runs when its configuration is uploaded and daily around 08:00 in Manila (00:00 UTC). GitHub may delay scheduled jobs.

If the upload interface omits the `.github` folder, choose **Add file → Create new file**, enter `.github/workflows/update-profile.yml` as the filename, paste the supplied workflow, and commit it. GitHub may ask you to enable Actions for the repository. No personal access token or extra secrets are required; the workflow uses GitHub's built-in token with repository contents write permission.

The checked-in images work immediately, even before the first automated run. Your repository is already public and named `httpsGabbae`, which is the profile repository for your username. These files have been prepared locally; they have not been published to your account.

## Personalize

Edit `profile.json` to change the name, role, stack, interests, and contact text. Keep values at most 48 characters so they fit. Your supplied portrait has been converted into `art/portrait-dark.txt` and `art/portrait-light.txt`. Each is at most 60 columns and 46 rows. The daily updater preserves this artwork; the original photograph and image-processing dependencies are not needed. The README's accessible image description and links are edited separately.

The displayed numbers mean:

- Repositories: GitHub's public repository count, including forks; original repositories are the owned public repositories that are not forks.
- Stars: total stars on original public repositories.
- Followers: current public follower count.
- Top language: the most common primary language among original repositories, counted by repository, not by bytes or proficiency. Repositories without a detected language are excluded.

Private repositories, commit totals, and lines of code are not counted. Your existing README has been saved alongside the ZIP as `original-README.md` for easy restoration.

## Local refresh

With Python 3.12 or later, run `python scripts/update_profile.py` from this folder. No packages are needed. An optional `GITHUB_TOKEN` environment variable increases the API rate limit. API failures stop the update and leave the previous images intact.

The two themes use SVG text and shapes with no external image or statistics service. The layout is inspired by [Andrew6rant's terminal-style profile](https://github.com/Andrew6rant/Andrew6rant); the source and ASCII portrait here were created for httpsGabbae using your supplied photograph.
