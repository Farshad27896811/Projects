import React, { useEffect, useState } from 'react';
import './App.css';

const API_KEY = 'e58c9f49869a8a0cf4d0bd23df91f1c6';

function App() {
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!navigator.geolocation) {
      setError('مرورگر شما از موقعیت جغرافیایی پشتیبانی نمی‌کند.');
      setLoading(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        try {
          const res = await fetch(
            `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${API_KEY}&units=metric&lang=fa`
          );
          const data = await res.json();
          if (data.cod === 200) {
            setWeather(data);
          } else {
            setError(data.message);
          }
        } catch (err) {
          setError('خطا در دریافت اطلاعات هواشناسی');
        } finally {
          setLoading(false);
        }
      },
      (err) => {
        setError('دسترسی به موقعیت مکانی رد شد.');
        setLoading(false);
      }
    );
  }, []);

  if (loading) return <div className="App">در حال بارگذاری...</div>;
  if (error) return <div className="App">❌ {error}</div>;

  return (
    <div className="App">
      <div className="weather-card">
        <h2>{weather.name}</h2>
        <img
          src={`https://openweathermap.org/img/wn/${weather.weather[0].icon}@2x.png`}
          alt={weather.weather[0].description}
        />
        <h3>{Math.round(weather.main.temp)}°C</h3>
        <p>{weather.weather[0].description}</p>
        <p>رطوبت: {weather.main.humidity}%</p>
        <p>سرعت باد: {weather.wind.speed} m/s</p>
      </div>
    </div>
  );
}

export default App;