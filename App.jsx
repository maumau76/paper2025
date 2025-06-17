import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/*"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="materials" element={<div>Materiais - Em desenvolvimento</div>} />
            <Route path="products" element={<div>Produtos - Em desenvolvimento</div>} />
            <Route path="inventory" element={<div>Estoque - Em desenvolvimento</div>} />
            <Route path="production" element={<div>Produção - Em desenvolvimento</div>} />
            <Route path="sales" element={<div>Vendas - Em desenvolvimento</div>} />
            <Route path="customers" element={<div>Clientes - Em desenvolvimento</div>} />
            <Route path="financial" element={<div>Financeiro - Em desenvolvimento</div>} />
            <Route path="reports" element={<div>Relatórios - Em desenvolvimento</div>} />
            <Route path="settings" element={<div>Configurações - Em desenvolvimento</div>} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;

