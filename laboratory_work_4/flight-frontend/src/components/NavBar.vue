<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <router-link class="navbar-brand" to="/">Табло рейсов</router-link>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="nav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item"><router-link class="nav-link" to="/">Рейсы</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/reviews">Отзывы</router-link></li>
          <li class="nav-item" v-if="isAuth"><router-link class="nav-link" to="/reservations">Мои брони</router-link></li>
          <li class="nav-item" v-if="isAuth"><router-link class="nav-link" to="/account">Аккаунт</router-link></li>
        </ul>

        <ul class="navbar-nav">
          <li class="nav-item" v-if="!isAuth"><router-link class="nav-link" to="/login">Войти</router-link></li>
          <li class="nav-item" v-if="!isAuth"><router-link class="nav-link" to="/register">Регистрация</router-link></li>
          <li class="nav-item" v-if="isAuth">
            <button class="btn btn-outline-light btn-sm" @click="logout">Выйти</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { logoutUser } from "../api/auth";

const router = useRouter();
const isAuth = computed(() => !!localStorage.getItem("auth_token"));

async function logout() {
  try { await logoutUser(); } catch (e) {}
  localStorage.removeItem("auth_token");
  router.push("/login");
  location.reload();
}
</script>
