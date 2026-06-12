# Code Review: `quantity_shade.py`

Here is my review of the provided helper file.

### 1. Logic Bug in Unit Conversions (Bug)
* **Where:** Line 18, `UNIT_FACTORS` dictionary.
* **Problem:** `"l": 100` maps liters to 100 ml. It should be `1000`. This will cause all liter-based inputs to be off by a factor of 10.
* **Change:** Update to `"l": 1000`.

### 2. Broken Promise on Range Clamping (Bug)
* **Where:** `shade_for()` function.
* **Problem:** The docstring promises: "The shade always stays inside the range [0.0, 1.0], so callers never have to clamp it themselves." However, `shade = base_amount / SHADE_CEILING` does not enforce a maximum. An input like "5 kg" returns `2.5`, breaking UI color calculations.
* **Change:** Clamp the return value: `return min(shade, 1.0)`.

### 3. Missing Common Unit Aliases (Enhancement)
* **Where:** `UNIT_FACTORS` dictionary.
* **Problem:** The dictionary is extremely strict. If a user types a common alias like "50 gm" or "2 ltr", the regex fails the dictionary lookup and falls through to Rule 3.
* **Change:** Add common aliases to the dictionary, such as `"gm": 1` and `"ltr": 1000`.

### 4. Low Shade Ceiling for Bulk (UX / Logic)
* **Where:** `SHADE_CEILING = 2000.0`
* **Problem:** The shade ceiling is capped at exactly 2 kg. If a user is bulk shopping for a family or business (e.g., "10 kg rice"), it reaches the maximum dark color instantly. 
* **Change:** Consider raising the ceiling to 5000.0 or implementing a logarithmic scale for shading rather than purely linear.

### 5. Production Memory Leak Risk (Architecture)
* **Where:** `_parse_cache = {}`
* **Problem:** This is an unbounded global dictionary. In a production server environment, if users type thousands of unique strings, this cache will grow infinitely and crash the server.
* **Change:** Replace with an LRU cache from Python's `functools` (`@lru_cache(maxsize=1000)`).