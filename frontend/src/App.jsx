
import { Link, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import PaymentResult from "./pages/PaymentResult";
import Orders from "./pages/Orders";

function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <Link to="/" className="brand">StyleHub</Link>
      <Link to="/">Shop</Link>

      {user && (
        <>
          <Link to="/cart">Cart</Link>
          <Link to="/orders">Orders</Link>
          <button onClick={logout}>Logout</button>
        </>
      )}

      {!user && (
        <>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
        </>
      )}
    </nav>
  );
}

function AppRoutes() {
  return (
    <>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/cart" element={<Cart />} />
          <Route path="/checkout" element={<Checkout />} />
          <Route path="/payment-result" element={<PaymentResult />} />
          <Route path="/orders" element={<Orders />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}