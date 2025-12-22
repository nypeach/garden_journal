===============================================
# 🌿 Master Garden ChatGPT Weather Assistant
_Last Updated: December 11, 2025 7:27 AM_
===============================================

Is it possible to get me the weather every morning at 6:00 AM?

Search for the National Weather Service point forecast for Loxahatchee, FL using the GPT web-browsing tool (no cached data) and this exact procedure, then reply in this chat:

1. Primary attempt (direct URL) - Open this URL: https://forecast.weather.gov/MapClick.php?lat=26.683680000000038&lon=-80.27976999999998

- If the page loads and contains the seven-day forecast tiles:
   - extract the first three tiles:
     - Tile 1: Today (condition + High temperature)
     - Tile 2: Tonight (condition + Low temperature)
     - Tile 3: Tomorrow (condition + High temperature)
   - But when a tile says something like: “Slight Chance of Showers” or “Chance of T-storms”
     - Replace that wording with the actual precipitation percentage pulled from the Detailed Forecast rows below the tiles (e.g., 20%, 10%, etc.).
   - If the wind gusts are expected to exceed 25 mph, include that information in the output alongside the standard Today/Tonight/Tomorrow format.

2. Retry on failure
- If the first attempt fails, retry up to three total attempts.

3. Fallback via location search

- If all direct attempts fail, search within forecast.weather.gov for "Loxahatchee, FL" and open the resulting point-forecast page.
- Extract the first three tiles as above.

4. If everything fails

- If both the direct URL (after 3 attempts) and the fallback search fail, return an error message. Do not invent or rewrite weather information.

5. Note formatting (when tile data is available)
- Use tile values verbatim. Do not hallucinate or summarize.
- Determine the current date in America/New_York, format it as mm/dd/yyyy, and insert it after the word "Today".
- Output must be a single markdown code block in exactly this format:

```markdown
Today {mm/dd/yyyy}: {Today condition} with a high of {Today High}°F dropping to {Tonight Low}°F overnight. {precipitation and wind gusts where applicable}. Tonight: {Tonight condition only}. Tomorrow: {Tomorrow condition} with a high of {Tomorrow High}°F.
```
6. After the code block, list the NWS page used as the source (direct URL or fallback URL).

7. Always perform a fresh web request. Never reuse weather data from previous runs.