<template>
  <div>
    <h1 class="mb-3">Рейсы</h1>

    <div class="row g-2 mb-3">
      <div class="col-sm-8">
        <input class="form-control" v-model="search" placeholder="Поиск: номер рейса, авиакомпания, город, гейт" />
      </div>
      <div class="col-sm-4">
        <button class="btn btn-primary w-100" @click="load()">Найти</button>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div class="table-responsive">
      <table class="table table-striped align-middle">
        <thead>
          <tr>
            <th>Номер</th>
            <th>Авиакомпания</th>
            <th>Маршрут</th>
            <th>Тип</th>
            <th>Гейт</th>
            <th>Вылет</th>
            <th>Прилёт</th>
            <th style="width: 170px;">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="f in flights" :key="f.id">
            <td><b>{{ f.flight_number }}</b></td>
            <td>{{ f.airline }}</td>
            <td>{{ f.departure_city }} → {{ f.arrival_city }}</td>
            <td>{{ f.flight_type === 'arrival' ? 'Прилёт' : 'Вылет' }}</td>
            <td>{{ f.gate }}</td>
            <td>{{ formatDT(f.departure_time) }}</td>
            <td>{{ formatDT(f.arrival_time) }}</td>
            <td>
              <button class="btn btn-success btn-sm" :disabled="!isAuth" @click="reserve(f.id)">
                Забронировать
              </button>
              <div class="text-muted small" v-if="!isAuth">Войдите, чтобы бронировать</div>
            </td>
          </tr>
          <tr v-if="flights.length === 0">
            <td colspan="8" class="text-muted">Рейсов пока нет.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="d-flex gap-2" v-if="page.next || page.prev">
      <button class="btn btn-outline-secondary btn-sm" :disabled="!page.prev" @click="load(page.prev)">Назад</button>
      <button class="btn btn-outline-secondary btn-sm" :disabled="!page.next" @click="load(page.next)">Вперёд</button>
      <div class="text-muted small align-self-center">Всего: {{ page.count }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { listFlights } from "../api/flights";
import { createReservation } from "../api/reservations";

const search = ref("");
const flights = ref([]);
const error = ref("");
const page = ref({ next: null, prev: null, count: 0 });

const isAuth = computed(() => !!localStorage.getItem("auth_token"));

function formatDT(val) {
  if (!val) return "";
  return new Date(val).toLocaleString("ru-RU");
}

async function load(url = null) {
  error.value = "";
  try {
    if (!url) {
      const data = await listFlights(search.value.trim());
      flights.value = data.results ?? data;
      page.value = { next: data.next, prev: data.previous, count: data.count ?? flights.value.length };
      return;
    }
    const res = await fetch(url);
    const data = await res.json();
    flights.value = data.results ?? data;
    page.value = { next: data.next, prev: data.previous, count: data.count ?? flights.value.length };
  } catch (e) {
    error.value = "Не удалось загрузить рейсы. Проверьте backend и CORS.";
  }
}

async function reserve(flightId) {
  const seat = prompt("Введите место (например A12):");
  if (!seat) return;
  try {
    await createReservation(flightId, seat);
    alert("Бронь создана! Откройте 'Мои брони'.");
  } catch (e) {
    alert("Не удалось создать бронь. Проверьте вход и токен.");
  }
}

load();
</script>
