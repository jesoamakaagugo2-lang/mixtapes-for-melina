# Mixtapes for Melina: self-updating setup

Every day, GitHub reads your YouTube Music playlists and rebuilds the site. Change a playlist and the site follows within a day (or instantly if you press "Run workflow").

## One-time setup (about 20 minutes)

1. **Get a YouTube API key (free).** Go to console.cloud.google.com, create a project, search for "YouTube Data API v3" and click Enable. Then Credentials, Create credentials, API key. Copy the key.
2. **Make a GitHub repository.** Create a new **public** repo (Pages is free for public repos). Upload every file from this folder. Hidden folders can be skipped by the uploader, so if `.github/workflows/update.yml` is missing, use Add file, Create new file, type `.github/workflows/update.yml` as the name and paste the contents.
3. **Save the key as a secret.** Repo Settings, Secrets and variables, Actions, New repository secret. Name: `YOUTUBE_API_KEY`. Value: your key.
4. **Run it once.** Actions tab, "Update mixtapes", Run workflow. When it finishes, a `docs/index.html` file appears in the repo.
5. **Turn on the site.** Settings, Pages, Deploy from a branch, branch `main`, folder `/docs`, Save.

Your site will be at `https://YOUR-USERNAME.github.io/YOUR-REPO/`.

## Everyday use

- **Add playlist 4:** edit `config.json` and add `{"id": "THE_LIST_ID", "name": "Name to show"}` after the last playlist (mind the commas). The id is the part after `list=` in the playlist link, before any `&`.
- **Rename a playlist:** change its `name` in `config.json`.
- **Playlists must be Public or Unlisted.** Private ones can't be read.
- If the build ever fails, the old site stays up and the Actions tab shows the error.
