
import { Link, useSearchParams } from "react-router-dom";

export default function PaymentResult() {
  const [searchParams] = useSearchParams();
  const paymentIntent = searchParams.get("payment_intent");
  const redirectStatus = searchParams.get("redirect_status");

  return (
    <main className="page">
      <h1>Payment Result</h1>

      {redirectStatus === "succeeded" ? (
        <p>
          Payment confirmation received. Your order status will be verified
          by the backend.
        </p>
      ) : (
        <p>
          Payment status: {redirectStatus || "pending"}.
          Check your orders for the latest verified status.
        </p>
      )}

      {paymentIntent && <p>Payment reference: {paymentIntent}</p>}

      <Link to="/orders">View My Orders</Link>
    </main>
  );
}