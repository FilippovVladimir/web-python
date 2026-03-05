<template>
  <div style="max-width: 520px;">
    <h1 class="mb-3">Регистрация</h1>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="ok" class="alert alert-success">{{ ok }}</div>

    <form class="card card-body" @submit.prevent="submit">
      <div class="mb-3">
        <label class="form-label">Логин</label>
        <input class="form-control" v-model="username" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Пароль</label>
        <input class="form-control" type="password" v-model="password" required />
      </div>

      <button class="btn btn-primary" type="submit">Создать аккаунт</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { registerUser, loginUser } from "../api/auth";

const router = useRouter();
const username = ref("");
const password = ref("");
const error = ref("");
const ok = ref("");

async function submit() {
  error.value = "";
  ok.value = "";
  try {
    await registerUser(username.value.trim(), password.value);
    const data = await loginUser(username.value.trim(), password.value);
    localStorage.setItem("auth_token", data.auth_token);
    ok.value = "Аккаунт создан!";
    await router.push("/");
  } catch (e) {
    const data = e?.response?.data;
    error.value = data ? JSON.stringify(data) : "Не удалось зарегистрироваться.";
  } 
}
</script>
