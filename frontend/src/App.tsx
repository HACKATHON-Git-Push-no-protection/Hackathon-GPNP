import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LogsPage from "./pages/LogsPage";
import Navbar from "./components/Navbar";
import { Container } from "@mui/material";

const App: React.FC = () => {
  return (
    <Router>
      <Navbar />
      <Container>
        <Routes>
          <Route path="/" element={<LogsPage />} />
        </Routes>
      </Container>
    </Router>
  );
};

export default App;
