
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { cartApi } from "../services/api";

export default function Cart() {
  const [cart, setCart] = useState({ items: [], total_cents: 0 });
  const [error, setError] = useState("");

  async function loadCart() {
    try {
      const response = await cartApi.get();
      setCart(response.data);
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load cart.");
    }
  }

  useEffect(() => {
    loadCart();
  }, []);

  async function changeQuantity(item, quantity) {
    if (quantity < 1) {
      await removeItem(item.id);
      return;
    }

    try {
      await cartApi.update(item.id, quantity);
      await loadCart();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to update quantity.");
    }
  }

  async function removeItem(itemId) {
    try {
      await cartApi.remove(itemId);
      await loadCart();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to remove item.");
    }
  }

  return (
    <main className="page">
      <h1>Your Shopping Cart</h1>

      {error && <p className="error">{error}</p>}

      {cart.items.map((item) => (
        <article className="cart-item" key={item.id}>
          <h2>{item.product.name}</h2>
          <p>
            Unit price: ₹{(item.product.price_cents / 100).toFixed(2)}
          </p>

          <button onClick={() => changeQuantity(item, item.quantity - 1)}>
            −
          </button>

          <span> {item.quantity} </span>

          <button onClick={() => changeQuantity(item, item.quantity + 1)}>
            +
          </button>

          <p>
            Line total: ₹{(item.line_total_cents / 100).toFixed(2)}
          </p>

          <button onClick={() => removeItem(item.id)}>Remove</button>
        </article>
      ))}

      <h2>
        Total: ₹{(cart.total_cents / 100).toFixed(2)}
      </h2>

      {cart.items.length > 0 ? (
        <Link to="/checkout">Proceed to Checkout</Link>
      ) : (
        <p>Your cart is empty.</p>
      )}
    </main>
  );
}