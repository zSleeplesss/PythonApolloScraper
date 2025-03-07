# PythonApolloScraper
Web scraper using python selenium and specific name fields to target elements

Here is how this works:
1. Be connected to the internet
2. Make sure all libraries are installed and Google Chrome is available on your computer
2. Try running file main.py and logging into the terminal with your REAL credentials. If this window fails to properly launch and initialize, try running again
3. When prompted, enter your search queries followed by "esc" to end. It could look something like this

```
Enter a search query or type "esc" to end:

> Target Finance
> Bank of America AML
> Oracle Consulting
> esc

... code runs here ...

```
4. Check csv files to ensure data was recorded

Notes
- STILL VERY BUGGY!
- This does not use an API, it opens a headless browser window and scrapes and parses data
- Works completely automatically, however can be rather slow due to viewport
- Will usually throw an error when done, disregard and only look to files to validate program success
- All listings are already preset under location: United States
- **Requires subscription to Apollo service to use fully (stops at 5 pages for first query >5 and throws error)**
- Still needs to be updated to click and open emails
- Some columns still need to be fixed
- Cloudflare may detect a script is running on the browser, if this happens just wait and try again or use a VPN if you have one