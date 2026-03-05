import { http } from "./http";

export async function listReviews() {
  const res = await http.get("/api/reviews/");
  return res.data;
}

export async function createReview(payload) {
  const res = await http.post("/api/reviews/", payload);
  return res.data;
}

export async function deleteReview(id) {
  const res = await http.delete(`/api/reviews/${id}/`);
  return res.data;
}
