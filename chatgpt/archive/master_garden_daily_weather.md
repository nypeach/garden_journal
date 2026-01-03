===============================================
# 🌿 Master Garden ChatGPT Weather Assistant
_Last Updated: December 24, 2025 6:47 AM_
===============================================

Is it possible to get me the weather every morning at 6:00 AM?

Search for the National Weather Service point forecast for Loxahatchee, FL using the GPT web-browsing tool (no cached data) and this exact procedure, then reply in this chat:

1. Primary attempt (direct URL) - Open this URL:
https://forecast.weather.gov/MapClick.php?lat=26.683680000000038&lon=-80.27976999999998

- If the page loads and contains the seven-day forecast tiles:
  - extract the first three tiles:
    - Tile 1: Today (condition + High temperature)
    - Tile 2: Tonight (condition + Low temperature)
    - Tile 3: Tomorrow (condition + High temperature)

  - ✅ Precipitation rule (Detailed Forecast rows)
    - If any of the tiles include precipitation wording such as:
      - “Slight Chance of Showers”
      - “Chance of T-storms”
      - “Showers likely”
      - etc.
    - Then you MUST look at the corresponding **Detailed Forecast** row(s) for that same period and:
      - If an explicit percentage is present (e.g., “Chance of precipitation is 20%” or “A 10 percent chance…”),
        replace the vague tile wording with **that percentage** (e.g., “20% chance of precipitation”).
      - If no percentage is present in the Detailed Forecast row, do NOT invent or infer one; leave the tile wording as-is.

  - ✅ Wind rule (Detailed Forecast rows)
    - Check the **Detailed Forecast** row(s) for wind information.
    - Only if wind gusts are explicitly forecast to exceed **25 mph** (e.g., “gusts as high as 30 mph”),
      include that gust value in the output.
    - If gusts are not mentioned or are ≤ 25 mph, do not include gusts.

2. Retry on failure
- If the first attempt fails, retry up to three total attempts.

3. Fallback via location search
- If all direct attempts fail, search within forecast.weather.gov for:
  - "Loxahatchee, FL"
  - OR use ZIP code "33470"
- Open the resulting NWS point-forecast page.
- Extract the first three tiles as above and apply the same precipitation + wind rules.

4. If everything fails
- If both the direct URL (after 3 attempts) and the fallback search fail, return an error message.
- Do not invent or rewrite weather information.

5. Note formatting (when tile data is available)
- Use tile values verbatim. Do not hallucinate or summarize.
- Determine the current date in America/New_York, format it as mm/dd/yyyy,
  and insert it after the word "Today".
- Output must be a single markdown code block in exactly this format:

```markdown
Today {mm/dd/yyyy}: {Today condition} with a high of {Today High}°F dropping to {Tonight Low}°F overnight. {precipitation % and wind gusts where applicable}. Tonight: {Tonight condition only}. Tomorrow: {Tomorrow condition} with a high of {Tomorrow High}°F.
