import React, { useState, useEffect } from 'react';
import './App.css';

const FILTERS = {
  all: () => true,
  completed: todo => todo.completed,
  incomplete: todo => !todo.completed,
};

function App() {
  const [todos, setTodos] = useState(() => {
    const saved = localStorage.getItem('todos');
    return saved ? JSON.parse(saved) : [];
  });
  const [filter, setFilter] = useState('all');
  const [text, setText] = useState('');
  const [category, setCategory] = useState('عمومی');
  const [date, setDate] = useState('');

  useEffect(() => {
    localStorage.setItem('todos', JSON.stringify(todos));
  }, [todos]);

  const addTodo = () => {
    if (!text || !date) return;
    const newTodo = {
      id: Date.now(),
      text,
      completed: false,
      category,
      date
    };
    setTodos([newTodo, ...todos]);
    setText('');
    setDate('');
  };

  const toggleTodo = id => {
    setTodos(todos.map(todo => todo.id === id ? { ...todo, completed: !todo.completed } : todo));
  };

  const removeTodo = id => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  return (
    <div className="App">
      <h1>📝 لیست کارها</h1>
      <div className="todo-form">
        <input value={text} onChange={e => setText(e.target.value)} placeholder="عنوان کار" />
        <input type="date" value={date} onChange={e => setDate(e.target.value)} />
        <select value={category} onChange={e => setCategory(e.target.value)}>
          <option value="عمومی">عمومی</option>
          <option value="شخصی">شخصی</option>
          <option value="کاری">کاری</option>
        </select>
        <button onClick={addTodo}>افزودن</button>
      </div>

      <div className="filters">
        {Object.keys(FILTERS).map(key => (
          <button
            key={key}
            onClick={() => setFilter(key)}
            className={filter === key ? 'active' : ''}
          >{key}</button>
        ))}
      </div>

      <ul className="todo-list">
        {todos.filter(FILTERS[filter]).map(todo => (
          <li key={todo.id} className={todo.completed ? 'done' : ''}>
            <div>
              <strong>{todo.text}</strong>
              <div>{todo.category} - {todo.date}</div>
            </div>
            <div className="actions">
              <button onClick={() => toggleTodo(todo.id)}>✓</button>
              <button onClick={() => removeTodo(todo.id)}>🗑️</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;