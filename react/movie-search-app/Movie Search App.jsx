// App.js
import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import MovieList from './components/MovieList';
import './App.css';

const API_KEY = 'YOUR_OMDB_API_KEY'; // کلید OMDB خود را اینجا قرار دهید

function App() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const searchMovies = async (query) => {
    if (!query) return;
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`https://www.omdbapi.com/?apikey=${API_KEY}&s=${query}`);
      const data = await res.json();
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

  return (
    <div className="App">
      <h1>🎬 جستجوی فیلم</h1>
      <SearchBar onSearch={searchMovies} />
      {loading && <p>در حال بارگذاری...</p>}
      {error && <p className="error">{error}</p>}
      <MovieList movies={movies} />
    </div>
  );
}

export default App;

// components/SearchBar.js
import React, { useState } from 'react';

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="search-bar">
      <input
        type="text"
        placeholder="نام فیلم را وارد کنید..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button type="submit">جستجو</button>
    </form>
  );
}

export default SearchBar;

// components/MovieList.js
import React from 'react';
import MovieCard from './MovieCard';

function MovieList({ movies }) {
  if (!movies.length) return null;

  return (
    <div className="movie-list">
      {movies.map((movie) => (
        <MovieCard key={movie.imdbID} movie={movie} />
      ))}
    </div>
  );
}

export default MovieList;

// components/MovieCard.js
import React from 'react';

function MovieCard({ movie }) {
  return (
    <div className="movie-card">
      <img src={movie.Poster !== 'N/A' ? movie.Poster : '/no-image.png'} alt={movie.Title} />
      <h3>{movie.Title}</h3>
      <p>{movie.Year}</p>
    </div>
  );
}

export default MovieCard;

// App.css
.App {
  text-align: center;
  font-family: sans-serif;
  padding: 2rem;
  background: #f0f0f0;
  min-height: 100vh;
}

.search-bar {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-bar input {
  padding: 0.5rem;
  width: 250px;
}

.search-bar button {
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.movie-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.movie-card {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s ease;
}

.movie-card:hover {
  transform: scale(1.03);
}

.movie-card img {
  width: 100%;
  height: 270px;
  object-fit: cover;
  border-radius: 4px;
}

.error {
  color: red;
  font-weight: bold;
}
