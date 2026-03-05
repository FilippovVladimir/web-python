<template>
  <div style="max-width: 520px;">
    <h1 class="mb-3">Вход</h1>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <form class="card card-body" @submit.prevent="submit">
      <div class="mb-3">
        <label class="form-label">Логин</label>
        <input class="form-control" v-model="username" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Пароль</label>
        <input class="form-control" type="password" v-model="password" required />
      </div>

      <button class="btn btn-primary" type="submit">Войти</button>

      <div class="text-muted small mt-2">
        Если запускали seed в ЛР3: <b>user1 / 12345678</b>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { loginUser } from "../api/auth";

const router = useRouter();
const username = ref("");
const password = ref("");
const error = ref("");

async function submit() {
  error.value = "";
  try {
    const data = await loginUser(username.value.trim(), password.value);
    localStorage.setItem("auth_token", data.auth_token);
    await router.push("/");
  } catch (e) {
    error.value = "Не удалось войти. Проверь логин/пароль и что backend запущен.";
  }
}
</script>
