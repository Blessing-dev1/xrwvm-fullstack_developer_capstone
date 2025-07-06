// src/App.js
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPanel from "./components/Login/Login";
import Logout from "./components/Logout/Logout";
import Dealers from './components/Dealers/Dealers';
import Dealer from "./components/Dealers/Dealer"

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/logout" element={<Logout />} />
      {/* redirect any unknown route to home */}
      <Route path="*" element={<Navigate to="/" />} />
      <Route path="/dealers" element={<Dealers/>} />
      <Route path="/dealer/:id" element={<Dealer/>} />
    </Routes>
  );
}

export default App;
