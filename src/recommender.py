from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv
import math

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV file with proper type conversions for scoring."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert CSV strings to appropriate types for scoring calculations
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),  # 0-1 scale
                'tempo_bpm': int(row['tempo_bpm']),  # beats per minute
                'valence': float(row['valence']),  # 0-1 scale (upbeat to introspective)
                'danceability': float(row['danceability']),  # 0-1 scale
                'acousticness': float(row['acousticness']),  # 0-1 scale (acoustic to electronic)
            }
            songs.append(song)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences using 6-component algorithm; return (score, reasons)."""
    score = 0.0
    reasons = []

    # Part 1: Mood Match (Binary) — +0 or +2.0 points (highest priority)
    user_mood = user_prefs.get('mood') or user_prefs.get('favorite_mood')
    if user_mood and song['mood'] == user_mood:
        mood_score = 2.0
        score += mood_score
        reasons.append(f"mood match (+{mood_score})")

    # Part 2: Genre Match (Binary) — +0 or +1.0 points
    user_genre = user_prefs.get('genre') or user_prefs.get('favorite_genre')
    if user_genre and song['genre'] == user_genre:
        genre_score = 1.0
        score += genre_score
        reasons.append(f"genre match (+{genre_score})")

    # Part 3: Valence Similarity (Gaussian) — 0 to 1.5 points
    user_valence = user_prefs.get('valence')
    if user_valence is not None:
        diff = abs(song['valence'] - user_valence)
        valence_score = 1.5 * math.exp(-(diff ** 2) / (2 * 0.20 ** 2))
        score += valence_score
        reasons.append(f"valence match (+{valence_score:.2f})")

    # Part 4: Energy Similarity (Gaussian) — 0 to 1.4 points
    user_energy = user_prefs.get('energy') or user_prefs.get('target_energy')
    if user_energy is not None:
        diff = abs(song['energy'] - user_energy)
        energy_score = 1.4 * math.exp(-(diff ** 2) / (2 * 0.20 ** 2))
        score += energy_score
        reasons.append(f"energy match (+{energy_score:.2f})")

    # Part 5: Danceability (Gaussian) — 0 to 1.0 points
    user_danceability = user_prefs.get('danceability')
    if user_danceability is not None:
        diff = abs(song['danceability'] - user_danceability)
        dance_score = 1.0 * math.exp(-(diff ** 2) / (2 * 0.20 ** 2))
        score += dance_score
        reasons.append(f"danceability match (+{dance_score:.2f})")

    # Part 6: Acousticness (Gaussian) — 0 to 0.6 points
    user_acousticness = user_prefs.get('acousticness')
    if user_acousticness is not None:
        diff = abs(song['acousticness'] - user_acousticness)
        acoustic_score = 0.6 * math.exp(-(diff ** 2) / (2 * 0.25 ** 2))
        score += acoustic_score
        reasons.append(f"acousticness match (+{acoustic_score:.2f})")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs and return top K recommendations ranked by similarity score."""
    # Score all songs and build (song, score, explanation) tuples
    recommendations = [
        (song, score, "; ".join(reasons) if reasons else "no matches")
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    # Sort by score (highest first) and return top K
    return sorted(recommendations, key=lambda x: x[1], reverse=True)[:k]
