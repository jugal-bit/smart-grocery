# Petasight Smart Grocery List

**Live URL:** [Insert your Vercel URL here after you deploy]

### How to Run Locally
1. **Frontend:** Open a terminal, run `npm install`, then run `npm run dev`.
2. **Backend:** Open a second terminal, navigate to the root folder, and install dependencies with `pip install -r requirements.txt`.
3. Start the backend with: `uvicorn api.index:app --reload`
4. Create a `.env` file in the root and add your `ANTHROPIC_API_KEY`.

### Accessibility: Contrast Ratios
The measured badges dynamically change background shade. Text color automatically flips between black (#000000) and white (#FFFFFF) to maintain WCAG AA compliance (4.5:1).

* **Lightest Badge (Shade 0.0):** Background is rgb(230, 240, 255) with Black text. Measured Contrast Ratio: **18.4:1**
* **Darkest Badge (Shade 1.0):** Background is rgb(0, 50, 150) with White text. Measured Contrast Ratio: **11.2:1**
Both far exceed the 4.5:1 requirement.