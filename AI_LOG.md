# AI Use Log

**Tools Used:** Gemini

**Prompts that moved the work forward:**
1. *"I need to build a project and deploy it in vercel, all instructions are written properly in the pdf file. Build me the application as per the instruction."* -> This generated the initial architecture and React boilerplate.
2. *"no if items are there means salt, sugar, flour, rice, oil , thn it is staple list, eveen though it contains 2 kg or 2liter anything , it will be taken as staple."* -> This helped refine the business logic to prioritize Rule 2 over Rule 1.

**Moments where AI was wrong and I caught it:**
1. **Tech Stack Deviation:** The AI initially suggested using Next.js (App Router) for the Vercel deployment. I caught this and corrected it, insisting on a standard React (Vite) frontend paired with a Python backend so we could natively use the provided `quantity_shade.py` file without needlessly translating it or overcomplicating the frontend.
2. **Logic Override:** The AI initially programmed Rule 1 (Measured) to beat Rule 2 (Staple) for the "2 kg salt" edge case. I reviewed the requirements and corrected the AI to ensure the Hardcoded Staples logic caught the item first, guaranteeing staples are always categorized correctly regardless of volume.