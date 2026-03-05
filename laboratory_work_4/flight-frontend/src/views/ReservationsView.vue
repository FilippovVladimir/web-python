<template>
  <div>
    <h1 class="mb-3">Мои бронирования</h1>

    <div v-if="!isAuth" class="alert alert-warning">
      Нужно войти, чтобы видеть бронирования.
      <router-link to="/login">Войти</router-link>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div class="table-responsive" v-if="isAuth">
      <table class="table table-striped align-middle">
        <thead>
          <tr>
            <th>ID</th>
            <th>Рейс (id)</th>
            <th>Место</th>
            <th>Билет</th>
            <th>Создано</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in reservations" :key="r.id">
            <td>{{ r.id }}</td>
            <td>{{ r.flight }}</td>
            <td><b>{{ r.seat }}</b></td>
            <td>{{ r.ticket_number || "—" }}</td>
            <td>{{ formatDT(r.created_at) }}</td>
            <td class="text-end">
              <button class="btn btn-outline-danger btn-sm" @click="remove(r.id)">Удалить</button>
            </td>
          </tr>
          <tr v-if="reservations.length === 0">
            <td colspan="6" class="text-muted">Пока нет бронирований.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="text-muted small" v-if="isAuth">
      * По API бронирования видны только владельцу (по токену).
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { listReservations, deleteReservation } from "../api/reservations";

const reservations = ref([]);
const error = ref("");

const isAuth = computed(() => !!localStorage.getItem("auth_token"));

function formatDT(val) {
  if (!val) return "";
  return new Date(val).toLocaleString("ru-RU");
}

async function load() {
  error.value = "";
  if (!isAuth.value) return;
  try {
    const data = await listReservations();
    reservations.value = data.results ?? data;
  } catch (e) {
    error.value = "Не удалось загрузить брони. Проверьте токен и CORS.";
  }
}

async function remove(id) {
  if (!confirm("Удалить бронь?")) return;
  try {
    await deleteReservation(id);
    await load();
  } catch (e) {
    alert("Не удалось удалить бронь.");
  }
}

load();
</script>
