import { useState, useEffect } from "react";
import reactLogo from "./assets/react.svg";
import fastApiLogo from "./assets/fastapi.svg";
import { invoke } from "@tauri-apps/api/tauri";
import { fetch } from "@tauri-apps/api/http";

import "./App.css";

interface ApiResponse {
  message: string;
}

function App() {
  const [greetMsg, setGreetMsg] = useState("");
  const [name, setName] = useState("");
  const [apiMessage, setApiMessage] = useState("");

  async function greet() {
    setGreetMsg(await invoke("greet", { name }));
  }

  async function fetchFromApi() {
    try {
      const response = await fetch<ApiResponse>("http://localhost:8008/");
      const message = response.data.message;
      setApiMessage(message);
    } catch (error) {
      console.error("Error fetching from API:", error);
    }
  }

  useEffect(() => {
    fetchFromApi();
  }, []);

  return (
    <div className="container">
      <h1>Welcome to Tauri!</h1>

      <div className="row">
        <a href="https://vitejs.dev" target="_blank">
          <img src="/vite.svg" className="logo vite" alt="Vite logo" />
        </a>
        <a href="https://tauri.app" target="_blank">
          <img src="/tauri.svg" className="logo tauri" alt="Tauri logo" />
        </a>
        <a href="https://reactjs.org" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
        <a href="https://fastapi.tiangolo.com/" target="_blank">
          <img src={fastApiLogo} className="logo react" alt="FastApi logo" />
        </a>
      </div>

      <p>Click on the Tauri, Vite, React and FastApi logos to learn more.</p>

      <form
        className="row"
        onSubmit={(e) => {
          e.preventDefault();
          greet();
        }}
      >
        <input
          id="greet-input"
          onChange={(e) => setName(e.currentTarget.value)}
          placeholder="Enter a name..."
        />
        <button type="submit">Greet</button>
      </form>

      <p>{greetMsg}</p>

      <div>
        <h2>Message from FastAPI:</h2>
        <p>{apiMessage}</p>
        <button onClick={fetchFromApi}>Refresh API Message</button>
      </div>
    </div>
  );
}

export default App;
