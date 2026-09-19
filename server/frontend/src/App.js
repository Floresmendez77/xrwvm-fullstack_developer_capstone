import LoginPanel from "./components/Login/Login";
import RegisterPanel from "./components/Register/Register";
import Dealers from "./components/Dealers/Dealers";
import { Routes, Route, Navigate } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dealers" replace />} />
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<RegisterPanel />} />
    </Routes>
  );
}
export default App;