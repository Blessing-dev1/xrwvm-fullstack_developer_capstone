// src/App.js
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPanel from "./components/Login/Login";
import Logout from "./components/Logout/Logout";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/logout" element={<Logout />} />
      {/* redirect any unknown route to home */}
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

export default App;
