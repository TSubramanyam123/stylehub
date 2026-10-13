import {
  useState
} from "react";

import {
  Link,
  useNavigate
} from "react-router-dom";

import {
  useAuth
} from "../context/AuthContext";


export default function Register() {

  const {
    register
  } = useAuth();

  const navigate =
    useNavigate();


  const [
    form,
    setForm
  ] = useState({
    email: "",
    password: ""
  });


  const [
    confirm,
    setConfirm
  ] = useState("");


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


    if (
      form.password !== confirm
    ) {

      setError(
        "Passwords do not match"
      );

      return;
    }


    setLoading(true);


    try {

      await register(
        form.email,
        form.password
      );

      navigate("/");

    } catch (error) {

      setError(
        error.response?.data?.detail
        || "Registration failed"
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
          Create account
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


        <label>
          Confirm password

          <input
            type="password"
            required
            minLength="8"
            value={confirm}
            onChange={(event) =>
              setConfirm(
                event.target.value
              )
            }
          />

        </label>


        <button
          className="primary full"
          disabled={loading}
        >

          {loading
            ? "Creating..."
            : "Create account"}

        </button>


        <p>
          Already registered?{" "}
          <Link to="/login">
            Login
          </Link>
        </p>

      </form>

    </div>
  );
}