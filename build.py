"""Reads the playlists in config.json from the YouTube Data API and writes docs/index.html."""
import datetime, json, os, re, sys, urllib.error, urllib.parse, urllib.request


def api(path, **params):
    params["key"] = os.environ["YOUTUBE_API_KEY"]
    url = "https://www.googleapis.com/youtube/v3/" + path + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit("YouTube API error %s: %s" % (e.code, e.read().decode()[:400]))


def tracks(pid):
    out, token = [], None
    while True:
        extra = {"pageToken": token} if token else {}
        d = api("playlistItems", part="snippet", playlistId=pid, maxResults=50, **extra)
        for it in d.get("items", []):
            s = it["snippet"]
            if s["title"] in ("Deleted video", "Private video"):
                continue
            artist = re.sub(r"\s*-\s*Topic$", "", s.get("videoOwnerChannelTitle", ""))
            out.append([s["title"], artist, s["resourceId"]["videoId"]])
        token = d.get("nextPageToken")
        if not token:
            return out


def main():
    if not os.environ.get("YOUTUBE_API_KEY"):
        sys.exit("Missing YOUTUBE_API_KEY")
    cfg = json.load(open("config.json", encoding="utf-8"))
    data = []
    for p in cfg["playlists"]:
        t = tracks(p["id"])
        name = p.get("name")
        if not name:
            name = api("playlists", part="snippet", id=p["id"])["items"][0]["snippet"]["title"]
        data.append({"n": name, "id": p["id"], "t": t})
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = open("template.html", encoding="utf-8").read()
    html = html.replace("__PLAYLISTS__", blob).replace("__DATE__", datetime.date.today().isoformat())
    os.makedirs("docs", exist_ok=True)
    open("docs/index.html", "w", encoding="utf-8").write(html)
    print("Built", sum(len(d["t"]) for d in data), "songs across", len(data), "playlists")


if __name__ == "__main__":
    main()
