import {
  useState
} from "react";

import {
  Link,
  useLocation,
  useNavigate
} from "react-router-dom";

import {
  useAuth
} from "../context/AuthContext";


export default function Login() {

  const {
    login
  } = useAuth();

  const navigate =
    useNavigate();

  const location =
    useLocation();


  const [
    form,
    setForm
  ] = useState({
    email: "",
    password: ""
  });


  const [
    error,
    setError
  ] = useState("");


  const [
    loading,
    setLoading
  ] = useState(false);


  const submit = async (event) => {

    event.preventDefault();

    setError("");

    setLoading(true);


    try {

      await login(
        form.email,
        form.password
      );

      navigate(
        location.state?.from || "/"
      );

    } catch (error) {

      setError(
        error.response?.data?.detail
        || "Login failed"
      );

    } finally {

      setLoading(false);

    }
  };


  return (

    <div className="auth-page">

      <form
        className="auth-card"
        onSubmit={submit}
      >

        <p className="eyebrow">
          STYLEHUB
        </p>

        <h1>
          Welcome back
        </h1>


        {error && (
          <div className="error-box">
            {error}
          </div>
        )}


        <label>
          Email

          <input
            type="email"
            required
            value={form.email}
            onChange={(event) =>
              setForm({
                ...form,
                email:
                  event.target.value
              })
            }
          />

        </label>


        <label>
          Password

          <input
            type="password"
            required
            minLength="8"
            value={form.password}
            onChange={(event) =>
              setForm({
                ...form,
                password:
                  event.target.value
              })
            }
          />

        </label>


        <button
          className="primary full"
          disabled={loading}
        >

          {loading
            ? "Please wait..."
            : "Login"}

        </button>


        <p>
          New to StyleHub?{" "}
          <Link to="/register">
            Create an account
          </Link>
        </p>

      </form>

    </div>
  );
}