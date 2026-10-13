
import { useState } from "react";
import {
  Elements,
  PaymentElement,
  useElements,
  useStripe,
} from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js";
import { orderApi } from "../services/api";

const publishableKey =
  import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY;

const stripePromise = publishableKey
  ? loadStripe(publishableKey)
  : null;

function PaymentForm() {
  const stripe = useStripe();
  const elements = useElements();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    if (!stripe || !elements) return;

    setBusy(true);
    setError("");

    const { error: paymentError } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        return_url: `${window.location.origin}/payment-result`,
      },
    });

    if (paymentError) {
      setError(paymentError.message || "Payment failed.");
    }

    setBusy(false);
  }

  return (
    <form onSubmit={handleSubmit} className="auth-form">
      <PaymentElement />

      {error && <p className="error">{error}</p>}

      <button disabled={!stripe || busy}>
        {busy ? "Processing..." : "Pay securely"}
      </button>
    </form>
  );
}

export default function Checkout() {
  const [options, setOptions] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function startCheckout() {
    setBusy(true);
    setError("");

    try {
      const response = await orderApi.createPaymentIntent();

      setOptions({
        clientSecret: response.data.client_secret,
      });
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Could not start checkout. Check your cart and payment configuration."
      );
    } finally {
      setBusy(false);
    }
  }

  if (!stripePromise) {
    return (
      <main className="page">
        <h1>Checkout</h1>
        <p className="error">
          Configure VITE_STRIPE_PUBLISHABLE_KEY in frontend/.env.
        </p>
      </main>
    );
  }

  return (
    <main className="page">
      <h1>Secure Checkout</h1>

      {!options && (
        <button onClick={startCheckout} disabled={busy}>
          {busy ? "Preparing checkout..." : "Continue to Payment"}
        </button>
      )}

      {error && <p className="error">{error}</p>}

      {options && (
        <Elements stripe={stripePromise} options={options}>
          <PaymentForm />
        </Elements>
      )}
    </main>
  );
}