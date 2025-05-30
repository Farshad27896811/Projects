import React, { useEffect, useState } from "react";
import "./App.css";

const API_KEY = "e58c9f49869a8a0cf4d0bd23df91f1c6"; // کلید API خود را وارد کنید

function App() {
  const [coords, setCoords] = useState(null);
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState("");
  const [manualCity, setManualCity] = useState("");

  useEffect(() => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          console.log("✅ موقعیت مکانی دریافت شد:", latitude, longitude);
          setCoords({ lat: latitude, lon: longitude });
        },
        (err) => {
          console.warn("⚠️ موقعیت مکانی رد شد:", err.message);
          setError("دسترسی به موقعیت مکانی رد شد. لطفاً شهر را به صورت دستی وارد کنید.");
        }
      );
    }
  }, []);

  useEffect(() => {
    if (coords) {
      fetchWeatherByCoords(coords.lat, coords.lon);
    }
  }, [coords]);

  const fetchWeatherByCoords = async (lat, lon) => {
    try {
      const res = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric&lang=fa`
      );
      const data = await res.json();
      if (data.cod !== 200) throw new Error(data.message);
      console.log("✅ اطلاعات آب‌وهوا با مختصات:", data);
      setWeather(data);
      setError("");
    } catch (err) {
      console.error("❌ خطا در گرفتن آب‌وهوا با مختصات:", err.message);
      setError("خطا در دریافت اطلاعات آب و هوا.");
    }
  };

  const fetchWeatherByCity = async () => {
    if (!manualCity) return;
    try {
      const res = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?q=${manualCity}&appid=${API_KEY}&units=metric&lang=fa`
      );
      const data = await res.json();
      if (data.cod !== 200) throw new Error(data.message);
      console.log("✅ اطلاعات آب‌وهوا با نام شهر:", data);
      setWeather(data);
      setError("");
    } catch (err) {
      console.error("❌ خطا در گرفتن آب‌وهوا با نام شهر:", err.message);
      setError("شهر مورد نظر پیدا نشد یا مشکلی وجود دارد.");
    }
  };

  return (
    <div className="app">
      {error && <p className="error">❌ {error}</p>}

      {!coords && (
        <div className="manual-input">
          <input
            type="text"
            placeholder="نام شهر را وارد کنید..."
            value={manualCity}
            onChange={(e) => setManualCity(e.target.value)}
          />
          <button onClick={fetchWeatherByCity}>جستجوی آب‌وهوا</button>
        </div>
      )}

      {weather ? (
        <div className="weather">
          <h1>{weather.name}</h1>
          <h2>{Math.round(weather.main.temp)}°C</h2>
          <p>{weather.weather[0].description}</p>
          <img
            src={`https://openweathermap.org/img/wn/${weather.weather[0].icon}@2x.png`}
            alt="weather icon"
          />
        </div>
      ) : (
        !error && <p className="loading">در حال دریافت اطلاعات...</p>
      )}
    </div>
  );
}

export default App;