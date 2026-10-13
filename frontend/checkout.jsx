import {
  Elements,
  PaymentElement,
  useElements,
  useStripe
} from "@stripe/react-stripe-js";

import {
  loadStripe
} from "@stripe/stripe-js";

useEffect(() => {

  orderApi
    .createPaymentIntent()
    .then((response) => {

      setClientSecret(
        response.data.client_secret
      );

      setPublishableKey(
        response.data.publishable_key
      );

      setOrder(
        response.data.order
      );

    })
    .catch((error) => {

      setError(
        error.response?.data?.detail
        || "Could not start checkout"
      );

    });

}, []);

const stripePromise =
  loadStripe(
    publishableKey
    || import.meta.env
        .VITE_STRIPE_PUBLISHABLE_KEY
  );

<Elements
  stripe={stripePromise}
  options={{
    clientSecret
  }}
>
  <PaymentForm
    order={order}
  />
</Elements>

const {
  error,
  paymentIntent
} =
  await stripe.confirmPayment({

    elements,

    confirmParams: {

      return_url:
        `${window.location.origin}` +
        `/payment-result?order_id=${order.id}`
    },

    redirect: "if_required"
  });

  if (error) {

  setMessage(
    error.message
    || "Payment failed"
  );

}
else if (
  paymentIntent?.status
  === "succeeded"
) {

  navigate(
    `/payment-result?order_id=${order.id}`
  );
}
