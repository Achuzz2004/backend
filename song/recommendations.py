import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def reccomend_for_user(customer, Song, ListeningHistory):
    history = ListeningHistory.objects.filter(user=customer)

    if not history.exists():
        return Song.objects.all().order_by('?')[:5]

    last_song = history.order_by('-played_at').first().song

    songs_qs = Song.objects.all()

    data = []
    for song in songs_qs:
        genres = " ".join([g.title for g in song.genres.all()])
        artists = " ".join([a.user.first_name + " " + a.user.last_name for a in song.artists.all()])
        features = f"{song.title} {genres} {artists}"
        data.append({
            "id": song.id,
            "features": features
        })

    songs = pd.DataFrame(data)

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(songs['features'])

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    idx = songs[songs['id'] == last_song.id].index[0]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Top 5 similar songs (excluding the current)

    song_indices = [i[0] for i in sim_scores]
    recommended_ids = songs.iloc[song_indices]['id'].tolist()

    return Song.objects.filter(id__in=recommended_ids)
