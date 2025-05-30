import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import MovieList from './components/MovieList';
import MovieDetails from './components/MovieDetails';
import './App.css';

const API_KEY = '6c6052e0';

function App() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [favorites, setFavorites] = useState([]);

  const searchMovies = async (query) => {
    if (!query) return;
    setLoading(true);
    setError(null);
    setSelectedMovie(null);

    try {
      const res = await fetch(`https://www.omdbapi.com/?apikey=${API_KEY}&s=${query}`);
      const data = await res.json();
      console.log('جستجوی فیلم:', data);
      if (data.Response === 'True') {
        setMovies(data.Search);
      } else {
        setError(data.Error);
        setMovies([]);
      }
    } catch (err) {
      setError('خطا در دریافت اطلاعات');
      setMovies([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchMovieDetails = async (id) => {
    console.log('در حال دریافت جزئیات فیلم با ID:', id);
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`https://www.omdbapi.com/?apikey=${API_KEY}&i=${id}`);
      const data = await res.json();
      console.log('داده دریافت‌شده:', data);
      if (data.Response === 'True') {
        setSelectedMovie(data);
      } else {
        setError(data.Error);
      }
    } catch (err) {
      setError('خطا در دریافت اطلاعات');
    } finally {
      setLoading(false);
    }
  };

  const addToFavorites = (movie) => {
    if (!favorites.find(fav => fav.imdbID === movie.imdbID)) {
      setFavorites([...favorites, movie]);
    }
  };

  return (
    <div className="App">
      <h1>🎬 جستجوی فیلم</h1>
      <SearchBar onSearch={searchMovies} />
      {loading && <p>در حال بارگذاری جزئیات...</p>}
      {error && <p className="error">{error}</p>}

      {!loading && selectedMovie ? (
        <MovieDetails
          movie={selectedMovie}
          onClose={() => setSelectedMovie(null)}
        />
      ) : (
        <MovieList
          movies={movies}
          onSelect={fetchMovieDetails}
          onFavorite={addToFavorites}
        />
      )}

      {favorites.length > 0 && (
        <div className="favorites">
          <h2>🎯 علاقه‌مندی‌ها</h2>
          <MovieList movies={favorites} />
        </div>
      )}
    </div>
  );
}

export default App;
