# What is this?
1) Given a clan ID get all members, get all Onslaught PGCRs, and calculate basic stats for individual members:
   * total runs
   * total legend runs
   * total normal runs
   * successful legend runs
   * successful normal runs
   * success percent
   * kills
   * deaths
   * assists
   * score
   * duration


# How to use?
1) Install all required packages
   1) `python3 -m pip install pandas plotly pathos requests pretty_html_table bar-chart-race tqdm prettytable`
2) Set your API key as an environemnt variable `BUNGIE_API_KEY`.  Get the key [here](https://www.bungie.net/en/Application).
   1) Alternatively: Add your api key to `main.py`. For this, edit `# API_KEY = "123456789"`.
3) Edit your user info in `main.py`. Alternatively, you can also use command line parameters to set this.
   ```py
      # Manually set clan ID here
      CLAN_ID = 881267
   ```
4) Run the script `python3 main.py`.
   1) Complete example for clans: `BUNGIE_API_KEY=123456789012345    python3 main.py -c 174643`
   2) Complete example for individual user: `BUNGIE_API_KEY=123456789012345    python3 main.py -p 2 -m 4611686018470531562`
   2) Alternatively you can also specify just the script if you set variables manually: `python3 main.py`

# Where do I get my clan ID?
1) Go to https://www.bungie.net/7/en (or any other similar page)
2) Search for your clan
   1) Open your profile, open your clan page
   2) Search for clan by name directly
3) Look at the URL: `https://www.bungie.net/7/en/Clan/Profile/174643`
   In this case, `174643` is your clan ID
