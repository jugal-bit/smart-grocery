# AI Use Log

**Tools Used:** Gemini

**Prompts that moved the work forward:**
1. *"I need to build a project and deploy it in vercel, all instructions are written properly in the pdf file."* -> This generated the initial Next.js/React architecture.
2. *"if items are there means salt, sugar, flour, rice, oil , thn it is staple list, eveen though it contains 2 kg or 2liter anything , it will be taken as staple."* -> This helped refine the business logic to prioritize Rule 2 over Rule 1.
3. *"i pushed ocde still no logs are coming... frozen pizzza not showing anything"* -> Used the AI to debug silent 500/404 errors during Vercel deployment. It helped me write a `try/except` trick to print the backend Gemini error directly to the frontend UI so I could see the model was outdated.

**Moments where AI was wrong and I caught it:**
1. **Tech Stack Deviation:** The AI initially suggested using Next.js (App Router). I caught this and corrected it, insisting on a standard React (Vite) frontend paired with a Python backend so we could natively use the provided `quantity_shade.py` file without overcomplicating it.
2. **Logic Override:** The AI initially programmed Rule 1 (Measured) to beat Rule 2 (Staple) for the "2 kg salt" edge case. I reviewed the instructions and corrected the AI to ensure Staples are always categorized correctly regardless of volume.
3. **Missing Files on Vercel:** The AI initially forgot to tell me to put the `quantity_shade.py` file inside the `api` folder, which caused a Vercel import error. I noticed the file was missing/empty in my file tree, pointed it out to the AI, and we fixed the import path.