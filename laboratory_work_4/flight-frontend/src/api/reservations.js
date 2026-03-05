import { http } from "./http";

export async function listReservations() {
  const res = await http.get("/api/reservations/");
  return res.data;
}

export async function createReservation(flightId, seat) {
  const res = await http.post("/api/reservations/", { flight: flightId, seat });
  return res.data;
}

export async function deleteReservation(id) {
  const res = await http.delete(`/api/reservations/${id}/`);
  return res.data;
}
