<template>
  <span class="calendar_frame">
    <main class="frame">
      <section
        class="monthFrame"
      >
        <!--월간달력 구간-->
        <!-- 월간 달력 년 월 구간 / 양쪽 버튼 클릭시 월을 하나씩 이동 가능 + 날짜 더블클릭시 input 입력창이 나오며 해당 년월로 이동-->
        <div class="monthInfo">
          <button class="monthInfoBtn" @click="calendarData(-1)">◀</button>
          <span>
            <span
              :class="{ inputstatus: inputhTitle }"
              @dblclick="changeYearForm"
            >
              {{ year }}년
            </span>
            <span
              :class="{ inputstatus: inputhTitle }"
              @dblclick="changeMonthForm"
            >
              {{ month }}월
            </span>
          </span>
          <input
            :class="{ inputstatus: !inputhTitle }"
            type="number"
            min="1"
            v-model.number="changedYear"
            @keyup.enter="changeYearForm"
          />
          <input
            :class="{ inputstatus: !inputhTitle }"
            type="number"
            value="currentMonth"
            min="1"
            max="12"
            v-model.number="changedMonth"
            @keyup.enter="changeMonthForm"
          />

          <button class="monthInfoBtn" @click="calendarData(1)">▶</button>
        </div>

        <!-- 월간 달력 테이블 -->
        <table class="calendar">
          <thead>
            <th v-for="(weekday, idx) in weekName" :key="idx">
              <span v-if="idx === 0">{{ weekday }}</span>
              <span v-else>{{ weekday }}</span>
            </th>
          </thead>
          <tbody>
            <tr v-for="(date, idx) in dates" :key="idx">
              <td v-for="(day, idx2) in date" :key="idx2">
                <div class="calendarDay" @click="todaySchedule(day)">
                  {{ day }}
                  <div>
                    <GroupCalendarTodo
                      :year="year"
                      :month="month"
                      :day="day"
                      :dates="dates"
                      :propstodos="groupTodos"
                      @changeTemp="changeTemp"
                    />
                  </div>
                </div>

                <!-- 그외 -->
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- 오늘 할 일 부분 -->
      <article class="todayGroupTodo">
        <div class="todayGroupInfo">{{ selectedMonth }}월 {{ selectedDay }}일</div>
          <GroupTodayTodolist
            :day="selectedDay"
            :year="year"
            :month="selectedMonth"
          />
      </article>
    </main>
  </span>
</template>

<script>
import { readGroupTodo, } from "../../api/group.js";
import GroupTodayTodolist from "./GroupTodayTodolist";
import GroupCalendarTodo from "./GroupCalendarTodo.vue";
export default {
  name: "GroupCalendar",
  components: {
    GroupTodayTodolist,
    GroupCalendarTodo,
  },
  props: {
    groupinfo: Object,
  },
  data() {
    return {
      inputhTitle: false,
      isModalViewed: false,
      weekName: [
        "일요일",
        "월요일",
        "화요일",
        "수요일",
        "목요일",
        "금요일",
        "토요일",
      ],
      dates: [],
      currentYear: 0,
      currentMonth: 0,
      year: 0,
      month: 0,
      lastMonthStart: 0,
      nextMonthStart: 0,
      today: 0,
      modal: false,
      thisDay: 1,
      changedYear: this.year,
      changedMonth: this.month,
      weekCalendar: [],
      weekIdx: 0,
      MaximumWeek: 0,
      goToBack: false,
      calendarToggle: false,
      selectedMonth: 0,
      selectedDay: 0,
      groupTodos: {},
      dateInfo: null,
      c_month: null,
      c_day: null,
    };
  },
  created() {
    const date = new Date();
    this.currentYear = date.getFullYear();
    this.currentMonth = date.getMonth() + 1;
    this.selectedMonth = date.getMonth() + 1;
    this.year = this.currentYear;
    this.month = this.currentMonth;
    this.today = date.getDate();
    this.selectedDay = date.getDate();
    this.calendarData();
    this.pickWeek();
    this.defaultYearMonth();
    this.gettogglestate();
  },
  mounted () {
    this.getGroupTodoList();
  },
  methods: {
    changeTemp () {
      this.getGroupTodoList();
    },
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
    getGroupTodoList () {
      readGroupTodo(
        this.$route.query.groupid,
        (res) => {
          this.groupTodos = res.data.todolist;
        },
        (err) => {
          console.log(err)
        }
      )
    },
    calendarChange() {
      this.$store.commit("todoStore/changeCalendar");
      this.calendarToggle = this.$store.state.todoStore.calendartogglestate;
      // this.calendarToggle = !this.calendarToggle;
    },
    defaultYearMonth() {
      this.changedYear = this.year;
      this.changedMonth = this.month;
    },
    changeWeekly(arg) {
      if (arg < 0) {
        this.weekIdx -= 1;
      } else if (arg === 1) {
        this.weekIdx = Number(this.weekIdx);
        this.weekIdx += 1;
      }

      if (this.weekIdx < 0) {
        this.month -= 1;
        this.goToBack = true;
        if (this.month === 0) {
          this.year -= 1;
          this.month = 12;
          this.goToBack = true;
        }
      } else if (this.weekIdx == this.MaximumWeek) {
        this.month += 1;
        this.weekIdx = 0;
      }
      if (this.month > 12) {
        this.year += 1;
        this.month = 1;
        this.weekIdx = 0;
      }

      const [
        monthFirstDay,
        monthLastDate,
        lastMonthLastDate,
      ] = this.getFirstDayLastDate(this.year, this.month);
      this.dates = this.getMonthOfDays(
        monthFirstDay,
        monthLastDate,
        lastMonthLastDate
      );

      this.MaximumWeek = this.dates.length;
      if (this.goToBack) {
        this.weekIdx = this.MaximumWeek - 1;
      }
      this.weekCalendar = this.dates[this.weekIdx];
      this.goToBack = false;
    },
    pickWeek() {
      for (const weekIdx in this.dates) {
        for (const daily of this.dates[weekIdx]) {
          if (this.today === daily) {
            this.weekCalendar = this.dates[weekIdx];
            this.weekIdx = weekIdx;
          }
        }
      }
      this.MaximumWeek = this.dates.length;
    },
    changeYearForm() {
      this.inputhTitle = !this.inputhTitle;
      this.year = this.changedYear;
      const [
        monthFirstDay,
        monthLastDate,
        lastMonthLastDate,
      ] = this.getFirstDayLastDate(this.year, this.month);
      this.dates = this.getMonthOfDays(
        monthFirstDay,
        monthLastDate,
        lastMonthLastDate
      );
    },
    changeMonthForm() {
      this.inputhTitle = !this.inputhTitle;
      this.monthForm = !this.monthForm;
      this.month = this.changedMonth;
      const [
        monthFirstDay,
        monthLastDate,
        lastMonthLastDate,
      ] = this.getFirstDayLastDate(this.year, this.month);
      this.dates = this.getMonthOfDays(
        monthFirstDay,
        monthLastDate,
        lastMonthLastDate
      );
    },
    modalDisappear() {
      this.modal = false;
    },
    todaySchedule(day) {
      this.selectedMonth = this.month;
      this.selectedDay = day;
      this.thisDay = day;
    },
    calendarData(arg) {
      if (arg < 0) {
        this.month -= 1;
      } else if (arg === 1) {
        this.month += 1;
      }
      if (this.month === 0) {
        this.year -= 1;
        this.month = 12;
      } else if (this.month > 12) {
        this.year += 1;
        this.month = 1;
      }
      const [
        monthFirstDay,
        monthLastDate,
        lastMonthLastDate,
      ] = this.getFirstDayLastDate(this.year, this.month);
      this.dates = this.getMonthOfDays(
        monthFirstDay,
        monthLastDate,
        lastMonthLastDate
      );
    },
    getFirstDayLastDate(year, month) {
      const firstDay = new Date(year, month - 1, 1).getDay(); // 이번달 시작요일
      const lastDate = new Date(year, month, 0).getDate(); // 이번달 마지막 날짜
      let lastYear = year;
      let lastMonth = month - 1;
      if (month == 1) {
        // 1월의 경우 저번달은 작년 12월
        lastMonth = 12;
        lastYear -= 1;
      }
      const prevLastDate = new Date(lastYear, lastMonth, 0).getDate(); // 지난달 마지막 날짜
      return [firstDay, lastDate, prevLastDate];
    },
    getMonthOfDays(monthFirstDay, monthLastDate, prevMonthLastDate) {
      let day = 1;
      let prevDay = prevMonthLastDate - monthFirstDay + 1;
      const dates = [];
      let weekOfDays = [];
      while (day <= monthLastDate) {
        if (day === 1) {
          // 1일이 어느 요일인지에 따라 테이블에 그리기 위한 지난 셀의 날짜들을 구해야함
          for (let j = 0; j < monthFirstDay; j += 1) {
            weekOfDays.push("");
            // weekOfDays.push(prevDay); , 달력상에 지난 날짜 표현 x
            prevDay = prevDay + 1;
          }
        }
        weekOfDays.push(day);
        if (weekOfDays.length === 7) {
          // 일주일이 채워지면
          dates.push(weekOfDays);
          weekOfDays = []; //초기화
        }
        day += 1;
      }
      if (weekOfDays.length > 0) dates.push(weekOfDays); // 남은 날짜 추가
      this.nextMonthStart = weekOfDays[0]; // 이번 달 마지막 주에서 제일 작은 날짜
      return dates;
    },
    user_change_year_month() {
      this.inputhTitle = true;
    },
    gotoTitle() {
      this.inputhTitle = false;
    },
    gettogglestate() {
      this.calendarToggle = this.$store.state.todoStore.calendartogglestate;
    },
  },
  watch: {
    month() {
      if (0 < this.month < 10) {
        this.c_month = "0" + String(this.month);
      } else {
        this.c_month = String(this.month);
      }
    },
  },
};
</script>

<style>
.todayGroupTodo {
  width: 25%;
  height: 100%;
  overflow: auto;
  box-shadow: 0px 0px 10px 0.3px var(--color-gray-light);
  border: none;
  border-radius: 15px;
  background-color: var(--color-white);
}
.todayGroupInfo{
  margin: 10px;
  border-bottom: 1px solid;
}
</style>