TELUGU SONG CARDS - HOW TO USE
==============================
FOLDER "site"  = your website (upload this to GitHub Pages).
Everything else = the tools that make the next songs.

ONE-TIME SETUP
1. Make a free account at github.com (remember your username).
2. Click New repository. Name it: telugu-christian-songs  (Public). Create.
3. Click "uploading an existing file". Drag the CONTENTS of the "site" folder in (index.html, sitemap.xml, robots.txt, images, songs). Commit.
4. Repository Settings > Pages > Source: "Deploy from a branch" > main / (root) > Save.
5. Your site will be at https://YOUR-USERNAME.github.io/telugu-christian-songs/
6. Open config.json and replace YOUR-GITHUB-USERNAME with your username. Then ask Claude to rebuild (the sitemap needs the real address).
7. Google Search Console (search.google.com/search-console): Add property > URL prefix > your address. Verify (HTML file method: upload the file Google gives into the repository). Then Sitemaps > add "sitemap.xml".

EVERY DAY (10 more songs)
- Ask Claude "make today's 10 cards" (it runs: python3 build_site.py 10). progress.json remembers which songs are done.
- Upload the new files from "site" to GitHub again (images, songs, index.html, sitemap.xml).
