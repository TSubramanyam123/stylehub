
import { useEffect, useState } from "react";
import { productApi, cartApi } from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function Home() {
  const { user } = useAuth();
  const [products, setProducts] = useState([]);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    productApi.list()
      .then((response) => {
        const data = response.data;
        setProducts(Array.isArray(data) ? data : data.items ?? []);
      })
      .catch((err) => {
        setError(
          err.response?.data?.detail ||
          "Unable to load products. Check the backend."
        );
      });
  }, []);

  async function addToCart(productId) {
    if (!user) {
      setMessage("Please log in before adding items to your cart.");
      return;
    }

    try {
      await cartApi.add(productId, 1);
      setMessage("Product added to your cart.");
    } catch (err) {
      setMessage(
        err.response?.data?.detail || "Unable to add product."
      );
    }
  }

  return (
    <main className="page">
      <h1>Welcome to StyleHub</h1>
      <p>Discover your next favourite look.</p>

      {message && <p>{message}</p>}
      {error && <p className="error">{error}</p>}

      <section className="product-grid">
        {products.map((product) => (
          <article className="product-card" key={product.id}>
            {product.image_url && (
              <img src={product.image_url} alt={product.name} />
            )}

            <h2>{product.name}</h2>
            <p>{product.description}</p>
            <p>Category: {product.category}</p>
            <p>Stock: {product.stock}</p>
            <p>
              Price: ₹{(product.price_cents / 100).toFixed(2)}
            </p>

            <button
              disabled={!product.is_active || product.stock <= 0}
              onClick={() => addToCart(product.id)}
            >
              Add to Cart
            </button>
          </article>
        ))}
      </section>
    </main>
  );
}