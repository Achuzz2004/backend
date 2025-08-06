def reccomend_for_user(customer, Song, ListeningHistory):
    # ✅ Move heavy imports inside the function (important for deployment on Render)
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import linear_kernel

    # 🔍 Fetch listening history of the user
    history = ListeningHistory.objects.filter(user=customer)

    # 🎵 If no history, return random songs
    if not history.exists():
        return Song.objects.all().order_by('?')[:5]

    # 🎧 Get the last song the user listened to
    last_song = history.order_by('-played_at').first().song

    # 🎼 Fetch all songs to compare for recommendations
    songs_qs = Song.objects.all()

    # 📊 Prepare data for recommendation
    data = []
    for song in songs_qs:
        genres = " ".join([g.title for g in song.genres.all()])
        artists = " ".join([a.user.first_name + " " + a.user.last_name for a in song.artists.all()])
        features = f"{song.title} {genres} {artists}"
        data.append({
            "id": song.id,
            "features": features
        })

    # 🧠 Create DataFrame for vectorization
    songs = pd.DataFrame(data)

    # ✨ TF-IDF Vectorization
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(songs['features'])

    # 📈 Compute cosine similarity between all songs
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # 🎯 Get index of last listened song
    idx = songs[songs['id'] == last_song.id].index[0]

    # 📊 Get similarity scores and sort
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Top 5 similar songs (excluding the current)

    # 🎵 Fetch recommended song IDs
    song_indices = [i[0] for i in sim_scores]
    recommended_ids = songs.iloc[song_indices]['id'].tolist()

    # 🔁 Return recommended songs
    return Song.objects.filter(id__in=recommended_ids)
