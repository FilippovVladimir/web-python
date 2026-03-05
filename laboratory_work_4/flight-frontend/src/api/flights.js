import { http } from "./http";

export async function listFlights(search = "") {
  const params = {};
  if (search) params.search = search;
  const res = await http.get("/api/flights/", { params });
  return res.data; // pagination: {count,next,previous,results}
}
