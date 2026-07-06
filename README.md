# League of Legends Match Win Predictor

A comprehensive machine learning pipeline for predicting League of Legends match outcomes using post-game player statistics, team objective data, and position-preserving feature engineering with SHAP interpretability.


## 📋 Table of Contents

- [Overview](#overview)
- [Research Questions](#research-questions)
- [Key Findings](#key-findings)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Data Collection](#data-collection)
- [Usage](#usage)
- [Pipeline Stages](#pipeline-stages)
- [Results Summary](#results-summary)
- [Model Interpretability](#model-interpretability)
- [Limitations](#limitations)
- [Future Work](#future-work)
- [Citation](#citation)

---

## Overview

This project develops and validates a complete machine learning pipeline for predicting League of Legends match outcomes from post-game statistics. The pipeline transforms participant-level data (10 players per match) into position-aware match-level features, applies rigorous two-stage feature selection, trains and compares 10 models (8 individual + 2 ensembles), validates stability through 100-iteration analysis, and provides SHAP-based interpretability.

**Best Model Performance:**
- **Voting Regressor (VotR):** R² = 0.8704, Accuracy = 95.75%
- **CatBoost (CatB):** R² = 0.8684, Accuracy = 96.00%
- **Ridge Regression:** Accuracy = 96.50% (highest classification rate)

**Dataset:** 2,000 ranked solo/duo matches from EU Nordic & East (EUN1) server, collected via tier-stratified snowball sampling from Iron through Challenger tiers.

---

## Research Questions

| ID | Question |
|----|----------|
| **RQ1** | Can ML models accurately predict winning teams using post-game player statistics and position-preserving feature engineering? |
| **RQ2** | Which post-game features exhibit the strongest predictive power for match outcomes? |
| **RQ3** | How do different ML algorithms compare in predictive performance? |
| **RQ4** | Do ensemble strategies (bagging, voting) improve performance over individual models? |
| **RQ5** | How robust are models to variations in training data? |

---

## Key Findings

1. **Structures dominate predictions:** Turret losses exhibit SHAP values 10× larger than any combat or economic features
2. **Jungler deaths are the key combat metric:** The only traditional combat stat among top 15 features
3. **Runes are strategic signals:** 5 of 15 selected features are pre-game rune configurations
4. **Kills don't predict wins:** Traditional offensive statistics (kills, damage, gold) are notably absent from top predictors
5. **The Ridge Paradox:** Ridge achieves highest accuracy (96.5%) but lowest R² (0.755) due to conservative probability estimates
6. **Ensemble benefit is modest:** Voting improves R² by only 0.002 over best individual model (CatBoost)

---

## Project Structure

```
LOL-Match-Win-Predictor/
│
├── data/
│   └── data collected/
│       ├── player ids/          # Player PUUIDs by tier/division
│       ├── match ids/           # Collected match IDs
│       └── flattened/           # Final CSV datasets
│           ├── teams_stats_merged_*.csv
│           └── match_data_merged_*.csv
│
├── notebooks/
│   ├── 1_data_collection_player_ids.ipynb
│   ├── 2_data_collection_match_ids.ipynb
│   ├── 3_data_collection_match_data.ipynb
│   └── 4_model_training_evaluation.ipynb
│
├── output/
│   ├── model_comparison_results.csv
│   ├── feature_importance.csv
│   ├── selected_features.txt
│   ├── dataset_info.txt
│   ├── correlation_matrix_sulov.png
│   ├── top_features_correlation.png
│   ├── model_comparison.png
│   ├── stability_analysis_boxplots.png
│   ├── shap_feature_importance.png
│   └── shap_summary_plot.png
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Riot Games API Key ([Get one here](https://developer.riotgames.com/))

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/LOL-Match-Win-Predictor.git
cd LOL-Match-Win-Predictor

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Requirements

```
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
scikit-learn>=1.3.0
xgboost>=2.0.0
catboost>=1.2.0
matplotlib>=3.7.0
seaborn>=0.12.0
shap>=0.42.0
requests>=2.31.0
python-dotenv>=1.0.0
```

---

## Data Collection

### Step 1: Collect Player IDs

Uses Riot Games league endpoints to collect player PUUIDs stratified by tier and division.

```python
# Collect 10 players from each tier/division
low_tier_players = get_x_players_per_low_tier_rank_and_division(count=10)
high_tier_players = get_x_puuids_per_high_tier()

# Save and merge all player files
save_players_by_division_to_csv(low_tier_players)
all_players = merge_division_files()
```

### Step 2: Collect Match IDs

Uses player PUUIDs to retrieve match histories with division-level quotas.

```python
match_ids = collect_match_ids_from_players(
    api_key,
    region='europe',
    sub_region='eun1',
    matches_per_tier={
        'IRON': 50, 'BRONZE': 50, 'SILVER': 50, 'GOLD': 50,
        'PLATINUM': 50, 'EMERALD': 50, 'DIAMOND': 50,
        'MASTER': 200, 'GRANDMASTER': 200, 'CHALLENGER': 200
    }
)
```

### Step 3: Fetch and Flatten Match Data

Retrieves full match data for each match ID and flattens into CSV format.

```python
teams_stats, match_data, failed_matches = collect_and_flatten_match_data(
    region='europe',
    sub_region='eun1',
    max_retries=3
)
```

### Sampling Strategy: Tier-Stratified Snowball Sampling

| Tier | Divisions | Matches per Division | Total |
|------|-----------|---------------------|-------|
| Iron, Bronze, Silver, Gold | I, II, III, IV | 50 | 800 |
| Platinum, Emerald | I, II, III, IV | 50 | 400 |
| Diamond | I, II, III, IV | 50 | 200 |
| Master, Grandmaster, Challenger | I only | 200 | 600 |
| **Total** | **31 divisions** | — | **2,000** |

---

## Usage

### Running the Complete Pipeline

```python
# Set your API key as environment variable
export RIOT_API_KEY='RGAPI-YOUR-KEY-HERE'

# Run notebooks in order:
# 1. 1_data_collection_player_ids.ipynb
# 2. 2_data_collection_match_ids.ipynb
# 3. 3_data_collection_match_data.ipynb
# 4. 4_model_training_evaluation.ipynb
```

### Quick Start with Pre-Collected Data

If you have the CSV files ready:

```python
# Update these paths in the notebook
MATCH_DATA_PATH = "path/to/teams_stats_merged.csv"
PARTICIPANT_DATA_PATH = "path/to/match_data_merged.csv"

# Run the model training notebook
# 4_model_training_evaluation.ipynb
```

---

## Pipeline Stages

### 1. Data Preprocessing
- Remove data leakage columns (player IDs, direct win indicators)
- Remove redundant and sparse features
- Median imputation for missing values
- Numeric type standardization

### 2. Feature Engineering
- Assign T1/T2 team prefixes based on teamId ordering
- Create position-specific player identifiers (T1_TOP, T2_JUNGLE, etc.)
- Pivot participant data: 10 rows → 1 row per match
- Merge team-level objective data
- Result: **1,254 engineered features**

### 3. Feature Selection
**Stage 1 — SULOV Correlation Analysis:**
- Remove feature pairs with correlation > 0.81
- Keep feature with higher target correlation
- Result: **1,050 features** (16.3% reduction)

**Stage 2 — XGBoost Recursive Feature Elimination:**
- Train XGBoost, rank features by gain-based importance
- Select top 15 features
- Result: **15 features** (98.5% total reduction)

### 4. Model Training & Evaluation

**8 Individual Models:**
| Model | Type | Scaling Required |
|-------|------|-----------------|
| Random Forest (RF) | Bagging Ensemble | No |
| XGBoost (XGB) | Gradient Boosting | No |
| CatBoost (CatB) | Gradient Boosting | No |
| Gradient Boosting (GradB) | Gradient Boosting | No |
| K-Nearest Neighbors (KNNR) | Instance-Based | Yes |
| Support Vector Regressor (SVR) | Kernel Method | Yes |
| Ridge Regression | Linear (L2) | Yes |
| Multi-Layer Perceptron (MLPR) | Neural Network | Yes |

**2 Ensemble Models:**
- **Bagging Regressor (BagR):** Best base model × 10 bootstrap estimators
- **Voting Regressor (VotR):** Average of top 3 individual models

**Configuration:**
- GridSearchCV with 5-fold cross-validation
- 80/20 stratified train-test split
- Regression → Classification via 0.5 threshold
- 6 evaluation metrics: R², Accuracy, MAE, RMSD, MAD, MAPD

### 5. Stability Analysis
- 100 iterations with randomized data splits
- Models reinstantiated with optimized hyperparameters
- Mean ± standard deviation for all metrics

### 6. SHAP Interpretability
- TreeExplainer for tree-based models
- KernelExplainer for ensemble and non-tree models
- Bar plots (global importance) and beeswarm plots (directional effects)

---

## Results Summary

### Model Performance

| Model | R² | Accuracy | MAE | MAD |
|-------|-----|----------|-----|-----|
| **VotR** | **0.8704** | 95.75% | 0.0773 | 0.0116 |
| CatB | 0.8684 | 96.00% | 0.0890 | 0.0230 |
| BagR | 0.8644 | 95.75% | 0.0896 | 0.0193 |
| XGB | 0.8613 | 95.25% | 0.0872 | 0.0164 |
| GradB | 0.8538 | 94.75% | 0.0661 | 0.0064 |
| RF | 0.8527 | 95.25% | 0.0651 | 0.0000 |
| MLPR | 0.8335 | 95.25% | 0.1202 | 0.0611 |
| SVR | 0.8248 | 95.00% | 0.1357 | 0.0799 |
| KNNR | 0.8015 | 94.75% | 0.0925 | 0.0000 |
| Ridge | 0.7554 | **96.50%** | 0.1912 | 0.1497 |

### Stability Analysis (100 Iterations)

| Metric | CatBoost | XGBoost | Gradient Boosting |
|--------|----------|---------|-------------------|
| Accuracy | 95.52 ± 0.97% | 95.07 ± 1.01% | 95.31 ± 1.04% |
| R² | 0.8632 ± 0.0192 | 0.8599 ± 0.0203 | 0.8630 ± 0.0242 |
| MAE | 0.0907 ± 0.0072 | 0.0883 ± 0.0071 | **0.0698** ± 0.0074 |
| MAD | 0.0221 ± 0.0022 | 0.0159 ± 0.0023 | **0.0061** ± 0.0012 |

### Top 15 Selected Features

| Rank | Feature | Importance | Category |
|------|---------|------------|----------|
| 1 | turretsLost_T2_TOP | 0.1694 | Structure |
| 2 | turretsLost_T1_UTILITY | 0.1013 | Structure |
| 3 | perk_primary_rune_1_var1_T1_UTILITY | 0.0354 | Rune |
| 4 | largestKillingSpree_T2_BOTTOM | 0.0186 | Combat |
| 5 | perk_primary_rune_4_T2_MIDDLE | 0.0175 | Rune |
| 6 | magicDamageTaken_T1_BOTTOM | 0.0152 | Damage |
| 7 | perk_secondary_rune_1_var1_T1_UTILITY | 0.0142 | Rune |
| 8 | spell4Casts_T1_UTILITY | 0.0142 | Ability |
| 9 | inhibitorTakedowns_T1_BOTTOM | 0.0138 | Structure |
| 10 | perk_stat_flex_T2_TOP | 0.0138 | Rune |
| 11 | perk_primary_rune_4_T1_JUNGLE | 0.0133 | Rune |
| 12 | perk_primary_rune_4_var2_T2_MIDDLE | 0.0127 | Rune |
| 13 | obj_inhibitor_first_T1 | 0.0123 | Team Objective |
| 14 | deaths_T1_JUNGLE | 0.0120 | Combat |
| 15 | turretTakedowns_T1_MIDDLE | 0.0114 | Structure |

---

## Model Interpretability

### SHAP Analysis Highlights

- Turret losses dominate with SHAP values 10× larger than other features
- Rune configurations rank high in XGBoost importance but show low SHAP impact — useful for tree splitting but limited independent predictive power
- Directional effects confirm logical relationships: losing turrets → decreased win probability
- Discrete clustering in SHAP values reflects integer nature of turret/inhibitor counts

### The Ridge Paradox

Ridge Regression achieves the highest accuracy (96.5%) but lowest R² (0.755). This occurs because:
1. L2 regularization shrinks predictions toward moderate values (~0.3–0.7)
2. Predictions remain on the correct side of the 0.5 threshold → high accuracy
3. R² penalizes conservative predictions heavily → low R²

**Implication:** Choose evaluation metrics based on application needs — accuracy for pure classification, R² for probability calibration.

---

## Limitations

- **Single region:** Data from EU Nordic & East (EUN1) only; may not generalize to other regions
- **Specific time period:** Collected during 2024-2025 season; meta-game shifts from patches may affect future performance
- **Post-game only:** Uses complete match data; not applicable for real-time prediction
- **Observational:** Predictive association does not imply causation
- **Queue specific:** Ranked Solo/Duo only; patterns may differ in professional play or other game modes

---

## Future Work

- **Temporal features:** Incorporate match timeline data for real-time win probability estimation
- **Champion modeling:** Develop champion embeddings and interaction features for synergy/counter modeling
- **Cross-patch learning:** Implement transfer learning for adaptation to game balance updates
- **Causal discovery:** Move from predictive association to causal inference
- **Multi-region validation:** Expand data collection across Korean, North American, and Chinese servers
- **Deployment:** Build real-time inference tools for players, coaches, and broadcasters

---

## Citation

If you use this work in your research, please cite:

```bibtex
@article{hegazi2024lolprediction,
  title={From Player Statistics to Victory: A Comprehensive Machine Learning 
         Pipeline for League of Legends Match Outcome Prediction with 
         SHAP Interpretability},
  author={Hegazi, Ibrahim},
  journal={arXiv preprint},
  year={2024}
}
```


---

## Acknowledgments

- **Riot Games** for providing the official API and comprehensive match data
- **scikit-learn, XGBoost, CatBoost** teams for machine learning libraries
- **SHAP** team (Lundberg & Lee) for model interpretability tools
- **Reference papers:**
  - Chowdhury, Ahsan & Barraclough (2024) — Linear & ensemble LoL prediction
  - Bahrololloomi et al. (2023) — Role-aware player performance metrics
  - Maymin (2021) — Context-aware esports analytics
  - Lundberg & Lee (2017) — SHAP unified interpretability framework

---

## Contact

**Ibrahim Hegazi**

📧 ihegaziwork

🔗 [GitHub Repository](https://github.com/Ibrahim-Hegazi)

---

*Last updated: June 2024*
