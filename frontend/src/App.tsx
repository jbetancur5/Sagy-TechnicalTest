import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import InvoiceList from "./pages/InvoiceList";
import InvoiceDetail from "./pages/InvoiceDetail";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/invoices" element={<InvoiceList />} />
        <Route path="/invoice/:id" element={<InvoiceDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
