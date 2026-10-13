import {
  Link,
  useNavigate
} from "react-router-dom";

import {
  useAuth
} from "../context/AuthContext";


export default function Navbar() {

  const {
    user,
    logout
  } = useAuth();

  const navigate =
    useNavigate();


  const signOut = () => {

    logout();

    navigate("/");

  };


  return (

    <nav className="nav">

      <Link
        className="brand"
        to="/"
      >
        StyleHub
      </Link>


      <div className="nav-links">

        <Link to="/">
          Shop
        </Link>


        {user && (

          <>
            <Link to="/cart">
              Cart
            </Link>

            <Link to="/orders">
              Orders
            </Link>

            <button
              className="link-button"
              onClick={signOut}
            >
              Logout
            </button>
          </>

        )}


        {!user && (

          <>
            <Link to="/login">
              Login
            </Link>

            <Link to="/register">
              Register
            </Link>
          </>

        )}

      </div>

    </nav>
  );
}