import React from 'react';

function MovieCard({ movie, onAddFavorite, onSelectMovie }) {
  return (
    <div className="movie-card" onClick={() => onSelectMovie && onSelectMovie(movie.imdbID)}>
      <img src={movie.Poster !== 'N/A' ? movie.Poster : '/no-image.png'} alt={movie.Title} />
      <h3>{movie.Title}</h3>
      <p>{movie.Year}</p>
      {onAddFavorite && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onAddFavorite(movie);
          }}
        >
          ❤️ افزودن به علاقه‌مندی
        </button>
      )}
    </div>
  );
}

export default MovieCard;
