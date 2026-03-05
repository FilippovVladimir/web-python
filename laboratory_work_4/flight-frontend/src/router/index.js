import { createRouter, createWebHistory } from "vue-router";
import FlightsView from "../views/FlightsView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import ReservationsView from "../views/ReservationsView.vue";
import ReviewsView from "../views/ReviewsView.vue";
import AccountView from "../views/AccountView.vue";

const routes = [
  { path: "/", name: "flights", component: FlightsView },
  { path: "/login", name: "login", component: LoginView },
  { path: "/register", name: "register", component: RegisterView },
  { path: "/reservations", name: "reservations", component: ReservationsView },
  { path: "/reviews", name: "reviews", component: ReviewsView },
  { path: "/account", name: "account", component: AccountView },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
