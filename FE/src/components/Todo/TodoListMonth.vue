<template>
  <div class="todomonthshow">
    <span class="todomonthshowtemp" v-show="temp">
      <div class="monthcalendartodoItem"></div>
    </span>
  </div>
</template>

<script>

export default {
  name: "TodoList",
  props: {
    day: [Number, String],
    year: [Number, String],
    month: [Number, String],
    dates: Array,
    propstodos: Object,
  },
  data: function () {
    return {
      todos: null,
      dateInfo: null,
      temp: false,
      c_month: null,
      c_day: null,
      p_todos: {},
    };
  },
  methods: {
    createDateInfo() {
      if (String(this.month).length === 1) {
        this.c_month = "0" + String(this.month);
      } else {
        this.c_month = String(this.month);
      }
      if (String(this.day).length === 1) {
        this.c_day = "0" + String(this.day);
      } else {
        this.c_day = String(this.day);
      }
      this.dateInfo =
        String(this.year) + String(this.c_month) + String(this.c_day);
    },
    getTodoList() {
      if (this.dateInfo in this.p_todos) {
        this.todos = this.p_todos[this.dateInfo];
        this.temp = true;
      } else {
        this.todos = [];
        this.temp = false;
      }
    },
  },

  watch: {
    dates() {
      if (String(this.month).length === 1) {
        this.c_month = "0" + String(this.month);
      } else {
        this.c_month = String(this.month);
      }
      if (String(this.day).length === 1) {
        this.c_day = "0" + String(this.day);
      } else {
        this.c_day = String(this.day);
      }
      this.dateInfo =
        String(this.year) + String(this.c_month) + String(this.c_day);
      this.getTodoList();
    },
    propstodos() {
      this.p_todos = this.propstodos;
      this.getTodoList();
    },
  },
  created() {
    this.createDateInfo();
  },
};
</script>

<style scoped>
.todomonthshow {
  width: 100%;
}

.todomonthshowtemp {
  width: 100%;
}

.monthcalendartodoItem {
  width: 100%;
  height: 10px;
  border-radius: 5px;
  box-shadow: 0px 0px 10px 0.3px var(--light-gray);
  border: none;
  background-color: rgb(255, 145, 0);
  font-size: 2px;
  text-align: left;
  padding-left: var(--padding);
  color: wheat;
}
</style>