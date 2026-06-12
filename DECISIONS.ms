# Decisions

### The "2 kg salt" Conflict
The brief asks how to handle an item like "2 kg salt", which triggers both Rule 1 (quantity/unit) and Rule 2 (hardcoded staple).

**Decision:** Rule 2 (Staple) wins. The tag rendered will be the neutral gray "staple" tag.

**Reasoning:** A staple is a fundamental category of grocery item. If a user is buying salt, sugar, or flour, the primary identifier of that item is that it belongs in the pantry staples category, regardless of the volume they are buying. Tagging "2 kg salt" as merely "measured" strips away the most important context of the item. To implement this cleanly, the application evaluates the staple keyword check before the regex quantity check.

### Architecture Choice
Vite (React) was chosen for the frontend alongside a Python Serverless backend. This allows native integration of the provided `quantity_shade.py` logic without needing to rewrite it in JavaScript, while keeping the Claude LLM API call securely on the server side.