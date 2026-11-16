# RR Pressure Performance Analytics Dashboard

Interactive Streamlit dashboard for the SuPeRR Selector Season 2 Round 1 analysis.

## Contents
- `app.py` — dashboard application
- `data/top10_batters.csv` — aggregated top-10 batter ranking output
- `data/top10_bowlers.csv` — aggregated top-10 bowler ranking output
- `requirements.txt` — deployment dependencies

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Publish with Streamlit Community Cloud
1. Create a **new public GitHub repository** for this dashboard only.
2. Upload the contents of this folder (do not upload the original raw Data Pack, `delivery_pressure_dataset.csv`, or any raw ball-by-ball files).
3. Sign in to Streamlit Community Cloud using GitHub and choose **Create app**.
4. Select your repository, branch `main`, and main file path `app.py`.
5. Deploy. When deployment succeeds, Streamlit will provide a public `https://....streamlit.app` URL.
6. Open the URL in a private/incognito browser window to verify that it is publicly accessible, then paste that URL into the Unstop dashboard-link field.

## Competition data handling
The original competition data pack is proprietary and must not be shared or published. This dashboard package intentionally contains only the top-10 aggregated ranking CSVs and does not include raw ball-by-ball data or the delivery-level pressure dataset. Check the competition's rules before publishing any derived outputs publicly. If public display of derived rankings is not permitted, leave the optional dashboard URL blank and submit the PDF/PPT instead.

## Important interpretation
The pressure thresholds and composite weights are modelling choices described in the dashboard. Scores are relative within the eligible player pools and are not official Rajasthan Royals ratings or predictions of future performance.
