
import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach JWT automatically to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("stylehub_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Authentication APIs
export const authApi = {
  register: (data) => api.post("/auth/register", data),
  login: (data) => api.post("/auth/login", data),
  me: () => api.get("/auth/me"),
};

// Product APIs
export const productApi = {
  list: () => api.get("/products"),
  get: (id) => api.get(`/products/${id}`),
};

// Cart APIs
export const cartApi = {
  get: () => api.get("/cart"),
  add: (product_id, quantity = 1) =>
    api.post("/cart/items", { product_id, quantity }),
  update: (itemId, quantity) =>
    api.patch(`/cart/items/${itemId}`, { quantity }),
  remove: (itemId) => api.delete(`/cart/items/${itemId}`),
};

// Order and payment APIs
export const orderApi = {
  createPaymentIntent: () =>
    api.post("/orders/create-payment-intent"),
  list: () => api.get("/orders"),
  get: (id) => api.get(`/orders/${id}`),
};

export default api;