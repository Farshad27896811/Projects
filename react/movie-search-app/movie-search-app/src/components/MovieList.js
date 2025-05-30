import React from 'react';
import MovieCard from './MovieCard';

function MovieList({ movies, onSelect, onFavorite }) {
  if (!movies || !movies.length) return null;

  return (
    <div className="movie-list">
      {movies.map((movie) => (
        <MovieCard
          key={movie.imdbID}
          movie={movie}
          onSelectMovie={onSelect}
          onAddFavorite={onFavorite}
        />
      ))}
    </div>
  );
}

export default MovieList;
