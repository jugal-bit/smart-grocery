# Code Review: `quantity_shade.py`

Here is my review of the provided helper file.

### 1. Logic Bug in Unit Conversions (Bug)
* **Where:** Line 18, `UNIT_FACTORS` dictionary.
* **Problem:** `"l": 100` maps liters to 100 ml. It should be `1000`. This will cause all liter-based inputs to be off by a factor of 10, resulting in badges that are much lighter than they should be.
* **Change:** Update to `"l": 1000`.

### 2. Broken Promise on Range Clamping (Bug)
* **Where:** Line 54, `shade_for()` function.
* **Problem:** The docstring promises: "The shade always stays inside the range [0.0, 1.0], so callers never have to clamp it themselves." However, `shade = base_amount / SHADE_CEILING` does not enforce a maximum. An input like "5 kg" (5000g) returns `2.5`, which will break UI color calculations expecting a max of 1.0.
* **Change:** Change line 62 to `return min(shade, 1.0)`.

### 3. Production Memory Leak Risk (Architecture Risk)
* **Where:** Line 24, `_parse_cache = {}`
* **Problem:** This is an unbounded global dictionary storing raw user input text. In a long-running production server environment, if thousands of users type unique strings, this cache will grow infinitely until the server runs out of memory and crashes.
* **Change:** Replace the basic dictionary with an LRU (Least Recently Used) cache from Python's `functools` (`@lru_cache(maxsize=1000)`) to ensure the memory footprint remains stable.

### 4. Brittle Regex (Nitpick)
* **Where:** Line 37, `re.match(r"\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)", text)`
* **Problem:** While functional for the happy path, this regex will fail or behave unexpectedly if a user inputs something with special characters or numbers attached to the unit (e.g., "500ml2"). 
* **Change:** Add boundary checks or make the unit capture group more specific to known units.