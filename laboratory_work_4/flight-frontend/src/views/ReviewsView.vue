<template>
  <div>
    <h1 class="mb-3">Отзывы</h1>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div class="row g-3">
      <div class="col-lg-7">
        <div class="list-group">
          <div class="list-group-item" v-for="rev in reviews" :key="rev.id">
            <div class="d-flex justify-content-between">
              <div>
                <b>Рейс:</b> {{ rev.flight }} |
                <b>Дата:</b> {{ rev.flight_date }} |
                <b>Рейтинг:</b> {{ rev.rating }}/10
              </div>
              <button class="btn btn-sm btn-outline-danger" v-if="isAuth" @click="remove(rev.id)">
                Удалить
              </button>
            </div>
            <div class="mt-2">{{ rev.text }}</div>
            <div class="text-muted small mt-2">Автор (id): {{ rev.author }}</div>
          </div>
          <div class="list-group-item text-muted" v-if="reviews.length === 0">
            Отзывов пока нет.
          </div>
        </div>
      </div>

      <div class="col-lg-5">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Добавить отзыв</h5>

            <div v-if="!isAuth" class="alert alert-warning mb-0">
              Нужно войти, чтобы оставлять отзывы.
              <router-link to="/login">Войти</router-link>
            </div>

            <form v-else @submit.prevent="submit">
              <div class="mb-2">
                <label class="form-label">ID рейса</label>
                <input class="form-control" v-model.number="flightId" type="number" min="1" required />
              </div>
              <div class="mb-2">
                <label class="form-label">Дата рейса</label>
                <input class="form-control" v-model="flightDate" type="date" required />
              </div>
              <div class="mb-2">
                <label class="form-label">Рейтинг (1-10)</label>
                <input class="form-control" v-model.number="rating" type="number" min="1" max="10" required />
              </div>
              <div class="mb-2">
                <label class="form-label">Текст</label>
                <textarea class="form-control" v-model="text" rows="3" required></textarea>
              </div>
              <button class="btn btn-primary w-100" type="submit">Отправить</button>
            </form>
          </div>
        </div>

        <div class="text-muted small mt-2">
          Подсказка: ID рейса можно посмотреть на странице “Рейсы”.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { listReviews, createReview, deleteReview } from "../api/reviews";

const reviews = ref([]);
const error = ref("");

const isAuth = computed(() => !!localStorage.getItem("auth_token"));

const flightId = ref(1);
const flightDate = ref(new Date().toISOString().slice(0, 10));
const rating = ref(8);
const text = ref("Всё прошло отлично!");

async function load() {
  error.value = "";
  try {
    const data = await listReviews();
    reviews.value = data.results ?? data;
  } catch (e) {
    error.value = "Не удалось загрузить отзывы.";
  }
}

async function submit() {
  try {
    await createReview({
      flight: flightId.value,
      flight_date: flightDate.value,
      rating: rating.value,
      text: text.value,
    });
    await load();
    alert("Отзыв добавлен!");
  } catch (e) {
    alert("Не удалось добавить отзыв. Проверьте токен и ID рейса.");
  }
}

async function remove(id) {
  if (!confirm("Удалить отзыв?")) return;
  try {
    await deleteReview(id);
    await load();
  } catch (e) {
    alert("Не удалось удалить отзыв.");
  }
}

load();
</script>
