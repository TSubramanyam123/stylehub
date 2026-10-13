
import { useEffect, useState } from "react";
import { orderApi } from "../services/api";

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    orderApi.list()
      .then((response) => {
        setOrders(response.data);
      })
      .catch((err) => {
        setError(err.response?.data?.detail || "Unable to load orders.");
      });
  }, []);

  return (
    <main className="page">
      <h1>My Orders</h1>

      {error && <p className="error">{error}</p>}

      {orders.map((order) => (
        <article className="order-card" key={order.id}>
          <h2>Order #{order.id}</h2>
          <p>Status: {order.status}</p>
          <p>
            Total: ₹{(order.total_cents / 100).toFixed(2)}
          </p>

          {order.items?.map((item, index) => (
            <p key={`${order.id}-${index}`}>
              {item.product_name} × {item.quantity}
            </p>
          ))}
        </article>
      ))}

      {orders.length === 0 && !error && <p>No orders found.</p>}
    </main>
  );
}