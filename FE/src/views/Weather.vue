<template>
  <div class="weather__frame">
    <div class="weather">
      <div class="weather__date">
        <span class="date">
          {{ today.year }}년 {{ today.month }}월 {{ today.date }}일
        </span>
      </div>

      <div class="weather__select">
        <label class="select__label" for="city-select">현재 위치: </label>
        <select
          class="select__option"
          name=""
          id="city-select"
          v-model="location"
          @change="getWeatherData(location)"
        >
          <option v-for="(coor, loc) in locations" :key="loc" :value="loc">
            {{ loc }}
          </option>
        </select>
      </div>

      <div class="weather__info">
        <h3 class="info__location">{{ location }}</h3>
        <span class="info__sky">{{ sky }}</span>
        <div class="info__detail">
          <div class="detail__icon">
            <i v-if="sky === '흐림'" class="fas fa-cloud"></i>
            <i v-else-if="sky === '비'" class="fas fa-cloud-showers-heavy"></i>
            <i v-else-if="sky === '구름 많음'" class="fas fa-cloud-sun"></i>
            <i v-else-if="sky === '눈'" class="fas fa-snowflake"></i>
            <i v-else-if="sky === '맑음'" class="fas fa-sun"></i>
          </div>
          <div class="detail__temp">
            <h3>{{ temp }}°C</h3>
          </div>
          <span class="info__pop">강수확률: {{ pop }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'Weather',
  data() {
    return {
      location: '서울', // 기본값: 서울
      active: true,
    };
  },
  computed: {
    ...mapState({
      locations: (state) => state.weatherStore.locations, // state 경로에 modules/<파일이름>, 모듈 변수의 이름이 아님..?!
      today: (state) => state.weatherStore.today,
      temp: (state) => state.weatherStore.temp,
      sky: (state) => state.weatherStore.sky,
      pop: (state) => state.weatherStore.pop,
    }),
  },
  methods: {
    getWeatherData(loc) {
      // console.log(this.$store);
      this.$store.dispatch('getWeatherData', loc);
    },
  },
  created() {
    this.getWeatherData(this.location);
  },
};
</script>

<style scoped src="@/assets/weather.css"></style>
