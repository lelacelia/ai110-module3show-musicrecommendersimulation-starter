# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

### 1. Narrow Gaussian Curves Create Energy/Valence/Danceability Filter Bubbles
The scoring algorithm uses very tight Gaussian distributions (σ=0.20) for energy, valence, and danceability. This means users with a preferred energy level of 0.5 will strongly favor songs in the 0.3–0.7 range but get almost zero points for songs outside 0.2 units away. For example, a calm-music lover (energy=0.3) will rarely discover upbeat dance tracks (energy=0.9) even if every other attribute matches perfectly. The narrow bands effectively lock users into their current preference zone, preventing discovery of songs across broader emotional or rhythmic spectrums. This creates invisible walls between music preference groups that should naturally overlap.

### 2. Mood Match (+2.0) Dominates as a Hard Filter
Mood matching awards the single largest bonus (+2.0 out of 7.5 max = 27% of total score) as a binary gate—you either get it or you don't. A song with no mood match must score at least 2.0 from the remaining five components just to tie with a mood-matched song that scores zero elsewhere. The mood feature also has representation problems: the 18-song catalog contains 14 different moods with only 1–3 songs per mood. This means most users will be effectively limited to recommending from a tiny subset (often 1–3 songs) regardless of how strong their preferences are in energy, genre, or danceability. The combination of high weight and low catalog coverage creates an unintentional mood-based echo chamber.

### 3. Genre Match (+1.0) Compounds the Mood Problem
Genre matching is another hard binary gate worth +1.0 points, which stacks on top of mood filtering. A user who prefers a specific mood AND genre may find themselves locked into a single song or completely locked out if that combination doesn't exist in the catalog. For instance, a user who wants "happy" mood and "jazz" genre will receive zero recommendations from the mood filter before genre is even considered. When both filters are combined, the effective catalog shrinks dramatically, reducing diversity in other important dimensions like energy or acousticness.

### 4. Acousticness Weighting Creates an Electronic Music Bias
Acousticness is weighted at only 0.6 out of 7.5 max—the lowest of all components—compared to energy (1.4) and danceability (1.0). This structural bias means users who strongly prefer acoustic instruments (folk, classical, unplugged) get smaller rewards for matches, while users who prefer electronic music face smaller penalties for mismatches. A classical music lover whose preferences align perfectly on mood, genre, energy, and danceability will still score lower than an electronic music lover with the same matches because the acousticness component contributes less. This unintentionally advantages electronic music recommendations over acoustic recommendations in the scoring hierarchy.

### 5. No Serendipity or Discovery Mechanism
The system is 100% exploitative—every recommendation directly matches stated preferences with no mechanism for beneficial surprise. Users never discover an artist they love in a mood they hadn't considered, or a new genre that shares their preferred tempo and energy. This is particularly harmful for users in niche categories (e.g., wanting rare moods like "angry" or "sensual") because the system cannot bridge to nearby moods even when audio features are nearly identical. The lack of any exploration component means the recommender reinforces narrow tastes rather than broadening musical horizons, which contradicts what many music discovery systems aim to do.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.


I ran different edge userprofiles to test how the model work (see model_card.md) - see 1 to 4 below. The issues that came out was:
**Issue 1**: Profile "Contradictory" uses mood "sad" which doesn't exist in any song

-The algorithm is working correctly (no mood match = 0 points)
But this profile can never score the +2.0 mood bonus because no song has mood="sad"
-Available moods: happy, chill, intense, moody, focused, laid-back, dark, sensual, serene, confident, romantic, euphoric, relaxed, energetic

**Issue 2**: Profile "Niche_conflicts" uses mood "angry" which also doesn't exist

-Same problem — no song in the catalog has mood="angry"
-This profile is severely handicapped, scoring only up to ~2.47/7.5 because it never gets the +2.0 mood bonus


**Surprise 1** Profile "acoustic_electronic_conflict" performs best — Despite the name suggesting conflicting preferences, Profile 3 gets the highest absolute scores (6.94, 6.87). The lofi genre seems to bridge the gap perfectly. Either the "conflict" isn't as sharp as the label suggests, or your algorithm handles preference conflicts really well.

---

## Profile Pair Comparisons

### Comparison 1: Contradictory vs. extreme_maxed (Profiles 1 & 2)
**What changed**: Contradictory max score is 3.97/7.5; extreme_maxed jumps to 4.93/7.5 (+1.0 point).
**Why it makes sense**: Contradictory uses mood "sad" which doesn't exist in the catalog, so no songs ever trigger the +2.0 mood bonus. It relies entirely on audio feature matches (energy, danceability, valence, acousticness). extreme_maxed has the same mood ("happy") that appears in "Gym Hero" and "Storm Runner," instantly unlocking the +2.0 bonus for top songs. **This validates the algorithm**: both profiles match on pop/rock high-energy songs, but extreme_maxed scores 25% higher because it benefits from the mood filter that Contradictory can't access.

### Comparison 2: extreme_maxed vs. acoustic_electronic_conflict (Profiles 2 & 3)  
**What changed**: extreme_maxed max score is 4.93/7.5; acoustic_electronic_conflict reaches 6.94/7.5 (+2.0 points). The genre winners flip completely (pop/rock → lofi/ambient).
**Why it makes sense**: Both get the +2.0 mood bonus, but acoustic_electronic_conflict achieves it with lofi songs that *also* trigger a genre match (+1.0), stacking to +3.0 before audio features. extreme_maxed's top song (Gym Hero) gets mood (+2.0) but no genre match because the profile prefers maximized audio features rather than a specific genre. acoustic_electronic_conflict's internally contradictory preferences (wants acoustic AND electronic) find their resolution in lofi and ambient—genres that naturally blend both. **This validates the algorithm**: preferences that seem conflicting can actually produce better results when the catalog contains bridging genres.

### Comparison 3: acoustic_electronic_conflict vs. niche_conflicts (Profiles 3 & 4)
**What changed**: acoustic_electronic_conflict max score is 6.94/7.5; niche_conflicts crashes to 2.47/7.5 (-4.5 points, a 64% drop).
**Why it makes sense**: Both profiles have "conflicting" preferences, but acoustic_electronic_conflict's preferences (high/low acousticness, electronic qualities, focused mood) exist in the catalog—lofi songs satisfy all of them. niche_conflicts asks for mood "angry" (which doesn't exist) paired with niche genres (metal, k-pop) and low danceability, creating a triple penalty: no mood bonus, rare genre combinations, and audio features that almost never match. **This validates the algorithm**: it correctly identifies when user preferences align with catalog availability vs. when they don't. niche_conflicts isn't a failure—it's the system working correctly by showing that its preferences are genuinely hard to satisfy.

### Comparison 4: Contradictory vs. niche_conflicts (Both low-scoring)
**What changed**: Contradictory max score is 3.97/7.5; niche_conflicts is 2.47/7.5 (difference of 1.5 points).
**Why it makes sense**: Contradictory lacks mood match but has genre matches (pop, rock get +1.0) and strong audio feature alignment (energy ≥ 1.29 for top 3). niche_conflicts has almost no genre matches (only 1 song of 5 in results) and barely hits audio feature targets. Contradictory's preferences can be partially satisfied by the 7 songs that don't require mood; niche_conflicts' preferences map to only 1-2 compatible songs in the entire catalog. **This validates the algorithm**: it degrades gracefully—users with partially-missing preferences still get reasonable scores, but users with catalog-incompatible preferences get correctly deprioritized.




1.Profile ```Contradictory```
Loading songs from data/songs.csv...
Loaded songs: 18

======================================================================
🎵 TOP SONG RECOMMENDATIONS
======================================================================

1. Gym Hero
   Artist: Max Pulse | Genre: pop
   Score: 3.97/7.5
   Why this recommendation:
      • genre match (+1.0)
      • valence match (+0.01)
      • energy match (+1.38)
      • danceability match (+0.99)
      • acousticness match (+0.59)

2. Sunrise City
   Artist: Neon Echo | Genre: pop
   Score: 3.82/7.5
   Why this recommendation:
      • genre match (+1.0)
      • valence match (+0.00)
      • energy match (+1.29)
      • danceability match (+0.96)
      • acousticness match (+0.57)

3. Broken Wings
   Artist: Echo Storm | Genre: metal
   Score: 3.21/7.5
   Why this recommendation:
      • valence match (+1.05)
      • energy match (+1.38)
      • danceability match (+0.18)
      • acousticness match (+0.60)

4. Storm Runner
   Artist: Voltline | Genre: rock
   Score: 3.02/7.5
   Why this recommendation:
      • valence match (+0.38)
      • energy match (+1.40)
      • danceability match (+0.64)
      • acousticness match (+0.60)

5. Midnight in Tokyo
   Artist: Neon Pulse | Genre: k-pop
   Score: 2.89/7.5
   Why this recommendation:
      • valence match (+0.01)
      • energy match (+1.34)
      • danceability match (+0.99)
      • acousticness match (+0.55)

======================================================================


2.Profile ```extreme_maxed```

Loading songs from data/songs.csv...
Loaded songs: 18                                            
                                                           
======================================================================
🎵 TOP SONG RECOMMENDATIONS
======================================================================

1. Gym Hero
   Artist: Max Pulse | Genre: pop
   Score: 4.93/7.5
   Why this recommendation:
      • mood match (+2.0)
      • valence match (+0.77)
      • energy match (+1.32)
      • danceability match (+0.84)
      • acousticness match (+0.00)

2. Storm Runner
   Artist: Voltline | Genre: rock
   Score: 4.55/7.5
   Why this recommendation:
      • mood match (+2.0)
      • genre match (+1.0)
      • valence match (+0.05)
      • energy match (+1.27)
      • danceability match (+0.24)
      • acousticness match (+0.00)

3. Midnight in Tokyo
   Artist: Neon Pulse | Genre: k-pop
   Score: 2.81/7.5
   Why this recommendation:
      • valence match (+0.96)
      • energy match (+1.02)
      • danceability match (+0.84)
      • acousticness match (+0.00)

4. Sunrise City
   Artist: Neon Echo | Genre: pop
   Score: 2.60/7.5
   Why this recommendation:
      • valence match (+1.09)
      • energy match (+0.93)
      • danceability match (+0.58)
      • acousticness match (+0.00)

5. Rhythm of the Night
   Artist: Tropical Vibes | Genre: afrobeats
   Score: 2.51/7.5
   Why this recommendation:
      • valence match (+1.09)
      • energy match (+0.68)
      • danceability match (+0.70)
      • acousticness match (+0.04)

======================================================================


3.Profile ```acoustic_electronic_conflict```
Loading songs from data/songs.csv...
Loaded songs: 18

======================================================================
🎵 TOP SONG RECOMMENDATIONS
======================================================================

1. Midnight Coding
   Artist: LoRoom | Genre: lofi
   Score: 6.94/7.5
   Why this recommendation:
      • mood match (+2.0)
      • genre match (+1.0)
      • valence match (+1.43)
      • energy match (+1.29)
      • danceability match (+0.84)
      • acousticness match (+0.38)

2. Library Rain
   Artist: Paper Lanterns | Genre: lofi
   Score: 6.87/7.5
   Why this recommendation:
      • mood match (+2.0)
      • genre match (+1.0)
      • valence match (+1.32)
      • energy match (+1.06)
      • danceability match (+0.92)
      • acousticness match (+0.56)

3. Spacewalk Thoughts
   Artist: Orbit Bloom | Genre: ambient
   Score: 5.40/7.5
   Why this recommendation:
      • mood match (+2.0)
      • valence match (+1.13)
      • energy match (+0.76)
      • danceability match (+0.90)
      • acousticness match (+0.60)

4. Focus Flow
   Artist: LoRoom | Genre: lofi
   Score: 4.95/7.5
   Why this recommendation:
      • genre match (+1.0)
      • valence match (+1.36)
      • energy match (+1.24)
      • danceability match (+0.88)
      • acousticness match (+0.48)

5. Coffee Shop Stories
   Artist: Slow Stereo | Genre: jazz
   Score: 3.56/7.5
   Why this recommendation:
      • valence match (+0.86)
      • energy match (+1.13)
      • danceability match (+0.98)
      • acousticness match (+0.58)

======================================================================


4. Profile ```niche_conflicts```
Loading songs from data/songs.csv...
Loaded songs: 18

======================================================================
🎵 TOP SONG RECOMMENDATIONS
======================================================================

1. Broken Wings
   Artist: Echo Storm | Genre: metal
   Score: 2.47/7.5
   Why this recommendation:
      • valence match (+0.82)
      • energy match (+1.39)
      • danceability match (+0.26)
      • acousticness match (+0.00)

2. Midnight in Tokyo
   Artist: Neon Pulse | Genre: k-pop
   Score: 2.22/7.5
   Why this recommendation:
      • genre match (+1.0)
      • valence match (+0.00)
      • energy match (+1.20)
      • danceability match (+0.00)
      • acousticness match (+0.01)

3. Storm Runner
   Artist: Voltline | Genre: rock
   Score: 1.66/7.5
   Why this recommendation:
      • valence match (+0.25)
      • energy match (+1.37)
      • danceability match (+0.04)
      • acousticness match (+0.00)

4. Moonlit Waltz
   Artist: Classical Dreams | Genre: classical
   Score: 1.60/7.5
   Why this recommendation:
      • valence match (+0.00)
      • energy match (+0.02)
      • danceability match (+0.99)
      • acousticness match (+0.59)

5. Gym Hero
   Artist: Max Pulse | Genre: pop
   Score: 1.40/7.5
   Why this recommendation:
      • valence match (+0.01)
      • energy match (+1.39)
      • danceability match (+0.00)
      • acousticness match (+0.00)

======================================================================

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
