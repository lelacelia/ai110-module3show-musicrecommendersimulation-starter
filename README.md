# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.
**Real-world recommenders** (Spotify, YouTube) use:
- Collaborative filtering (what people like you enjoyed)
- Massive user behavior data (millions of plays/skips)
- Contextual signals (time of day, device, location)
- Engagement feedback loops (skips, replays, shares)
- Multiple objectives (engagement + discovery + fairness)

**My recommender** focuses on content-based similarity:
- **Mood/Vibe Match**: Does the song match my emotional state? (highest priority)
- **Genre Match**: Does it fit the same music category? (secondary filter)
- **Audio Feature Similarity**: How close are energy, valence, danceability, acousticness?

For every song, I calculate a similarity score by comparing it to the user's preferences using mood match, genre match, and audio feature analysis.


Some prompts to answer:

- What features does each `Song` use in your system
    id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness
- What information does your `UserProfile` store
**UserProfile** stores:
- `genre` — the user's preferred genre
- `energy` — how intense/loud they like songs (0-1)
- `danceability` — how rhythm-driven they like songs (0-1)
- `acousticness` — acoustic vs. electronic preference (0-1)
- `valence` — how upbeat/positive they like songs (0-1)
- `mood` — emotional tone preference (e.g., "happy", "chill")

These preferences are typically extracted from a song the user likes. 
The Recommender uses this profile as the "target" and scores every song 
in the catalog by comparing it to these preferences.

- How does your `Recommender` compute a score for each song

### Scoring Rule: Computing a Score for Each Song
The Recommender computes a **similarity score** for each song by comparing it to the user's profile. The score measures "how well does this song match what the user likes?" The score ranges from 0 (terrible match) to ~7.5 (perfect match).

**The scoring has 6 components:**

**Part 1: Mood Match (Binary) — +0 or +2.0 points**
- If song.mood == user.favorite_mood: +2.0 points (perfect emotional match)
- Otherwise: 0 points
- Example: User likes "chill" → chill songs get +2.0, energetic songs get 0

**Part 2: Genre Match (Binary) — +0 or +1.0 points**
- If song.genre == user.favorite_genre: +1.0 points
- Otherwise: 0 points
- Note: Genre is secondary; mood takes priority

**Part 3: Valence Similarity (Gaussian) — 0 to 1.5 points**
- Measures emotional positivity (upbeat vs introspective)
- Formula: `1.5 × e^(-(difference² / (2 × 0.20²)))`
- Tolerance: 0.20 (±0.20 variation is acceptable)

**Part 4: Energy Similarity (Gaussian) — 0 to 1.4 points**
- Measures intensity/loudness
- Formula: `1.4 × e^(-(difference² / (2 × 0.20²)))`
- Tolerance: 0.20

**Part 5: Danceability (Gaussian) — 0 to 1.0 points**
- Measures groove/rhythm-driven quality
- Formula: `1.0 × e^(-(difference² / (2 × 0.20²)))`
- Tolerance: 0.20

**Part 6: Acousticness (Gaussian) — 0 to 0.6 points**
- Measures acoustic vs electronic preference
- Formula: `0.6 × e^(-(difference² / (2 × 0.25²)))`
- Tolerance: 0.25 (looser tolerance—this is a nice-to-have)

**Part 7: Combine All Components**
```
total_score = mood_score + genre_score + valence_score + energy_score + dance_score + acoustic_score
```
Maximum possible score: ~7.5 (all components match perfectly)


- How do you choose which songs to recommend
### Ranking Rule: Choosing Which Songs to Recommend

After computing scores for every song in the catalog, I use a simple **ranking rule** 
to decide which ones to show the user:

**The Process:**

1. **Score all songs** using the scoring rule above
   - Every song gets a similarity score

2. **Sort by score** (highest to lowest)
   - Best matches go to the top
   - Worst matches go to the bottom

3. **Return top K songs** (usually 3 or 5)
   - We recommend the songs with the highest scores
   - If K=3, we return the top 3 songs


You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

**Potential Biases in This Algorithm:**

- **Mood label brittleness**: Songs labeled "relaxed" won't match users who prefer "chill," even though they're similar moods
- **Binary mood cutoff**: A non-matching mood gets 0 points, ignoring partial credit for similar emotional tones
- **Sonic whiplash**: Lowering genre weight might recommend reggae and indie pop together if moods/energy match, despite different production styles
- **No behavioral signals**: Ignores actual user listening behavior (skips, replays)—only uses static features

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



