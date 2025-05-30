import React from 'react';

function MovieDetails({ movie, onClose }) {
  if (!movie) return null;

  return (
    <div className="movie-details">
      <button className="close-btn" onClick={onClose}>❌ بستن</button>
      <h2>{movie.Title}</h2>
      <img src={movie.Poster !== 'N/A' ? movie.Poster : '/no-image.png'} alt={movie.Title} />
      <p><strong>سال:</strong> {movie.Year}</p>
      <p><strong>ژانر:</strong> {movie.Genre}</p>
      <p><strong>کارگردان:</strong> {movie.Director}</p>
      <p><strong>خلاصه:</strong> {movie.Plot}</p>
      <p><strong>امتیاز:</strong> {movie.imdbRating}</p>
    </div>
  );
}

export default MovieDetails;
