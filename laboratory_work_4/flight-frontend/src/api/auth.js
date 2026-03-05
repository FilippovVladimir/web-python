import { http } from "./http";

export async function registerUser(username, password) {
  const payload = { username, password, re_password: password };
  const res = await http.post("/api/auth/users/", payload);
  return res.data;
}

export async function loginUser(username, password) {
  const res = await http.post("/api/auth/token/login/", { username, password });
  return res.data; // { auth_token: "..." }
}

export async function logoutUser() {
  const res = await http.post("/api/auth/token/logout/");
  return res.data;
}

export async function getMe() {
  const res = await http.get("/api/auth/users/me/");
  return res.data;
}

export async function updateMe(payload) {
  const res = await http.patch("/api/auth/users/me/", payload);
  return res.data;
}
