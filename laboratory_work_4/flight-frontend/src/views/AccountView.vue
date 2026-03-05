<template>
  <div style="max-width: 720px;">
    <h1 class="mb-3">Аккаунт</h1>

    <div v-if="!isAuth" class="alert alert-warning">
      Нужно войти.
      <router-link to="/login">Войти</router-link>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="ok" class="alert alert-success">{{ ok }}</div>

    <div v-if="isAuth" class="card card-body">
      <div class="mb-3">
        <b>Текущий пользователь:</b>
        <div class="bg-light p-3 rounded mt-2">
          <p><b>ID:</b> {{ me?.id }}</p>
          <p><b>Логин:</b> {{ me?.username }}</p>
          <p><b>Email:</b> {{ me?.email || "—" }}</p>
        </div>
      </div>

      <h5>Изменить данные</h5>
      <form @submit.prevent="save">
        <div class="row g-2">
          <div class="col-md-6">
            <label class="form-label">Новый username</label>
            <input class="form-control" v-model="newUsername" />
          </div>
          <div class="col-md-6">
            <label class="form-label">Email</label>
            <input class="form-control" v-model="email" />
          </div>
        </div>
        <button class="btn btn-primary mt-3" type="submit">Сохранить</button>
        <div class="text-muted small mt-2">
          * Запрос отправляется на <code>/api/auth/users/me/</code> (Djoser).
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { getMe, updateMe } from "../api/auth";

const isAuth = computed(() => !!localStorage.getItem("auth_token"));
const me = ref(null);
const error = ref("");
const ok = ref("");

const newUsername = ref("");
const email = ref("");

async function load() {
  error.value = "";
  ok.value = "";
  if (!isAuth.value) return;
  try {
    me.value = await getMe();
    newUsername.value = me.value?.username || "";
    email.value = me.value?.email || "";
  } catch (e) {
    error.value = "Не удалось получить данные пользователя. Проверьте токен.";
  }
}

async function save() {
  error.value = "";
  ok.value = "";
  try {
    const payload = { email: email.value };
    if (newUsername.value) payload.username = newUsername.value;
    me.value = await updateMe(payload);
    ok.value = "Данные обновлены!";
  } catch (e) {
    error.value = "Не удалось обновить данные. Возможно, backend запрещает менять некоторые поля.";
  }
}

load();
</script>
