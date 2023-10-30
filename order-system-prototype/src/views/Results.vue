<template>
  <div class="section">
    <div class="navbar has-shadow">
      <div class="navbar-brand">
        <div class="navbar-item">
          <i class="fa fa-calendar-check-o m-4 has-text-primary is-size-1"></i>
          <p class="subtitle is-2">软件可用性评估工具</p>
        </div>
      </div>
      <div class="navbar-menu">
        <div class="navbar-start"></div>
        <div class="navbar-end">
          <i class="fa fa-language is-size-3 mx-3"></i>
          <i class="fa fa-github is-size-3 mx-3"></i>
          <i class="fa fa-commenting is-size-3 mx-3"></i>
          <i class="fa fa-info-circle is-size-3 mx-3"></i>
        </div>
      </div>
    </div>

    <div class="section" style="height: 100%">
      <div class="box my-box">
        <div class="tile is-ancestor">
          <div class="tile is-parent is-vertical">
            <div class="tile is-child" style="flex: 1">
              <p>
                <span
                  class="has-text-primary has-text-weight-bold is-size-2 m-5"
                  >Step 3</span
                >
                <span class="is-size-3">测试结果分析</span>
              </p>
            </div>
            <!-- <div
              class="tile is-child is-flex-direction-column is-align-items-center"
              style="flex: 8; display: flex"
            > -->
            <div class="tile is-child pl-6" style="flex: 8">
              <!-- margin/padding 的 suffix 只有从 0 (0) 到 6 (3 rem) 
              需要更大距离只能使用 style="margin-left=..." 之类的自己调节 -->
              <!-- <div class="content"><p>各维度得分明细：</p></div> -->
              <table
                class="table ml-6 is-striped is-hoverable has-text-centered"
                style="width: 70%"
              >
                <thead>
                  <!-- 
                    style="text-align: center" 
                    class="has-text-centered"
                    自己写一个CSS类选择器
                    都不行，
                    写到 <th> 里，成功了！
                  -->
                  <tr>
                    <th class="has-text-centered">评价维度</th>
                    <th class="has-text-centered">得分</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Accessibility</td>
                    <td>{{ scores.accessibility }}</td>
                  </tr>
                  <tr>
                    <td>Ease of use</td>
                    <td>{{ scores.easeOfUse }}</td>
                  </tr>
                  <tr>
                    <td>Accuracy</td>
                    <td>{{ scores.accuracy }}</td>
                  </tr>
                  <tr>
                    <td>Consistency</td>
                    <td>{{ scores.consistency }}</td>
                  </tr>
                  <tr>
                    <td>Device efficiency</td>
                    <td>{{ scores.deviceEfficiency }}</td>
                  </tr>
                  <tr>
                    <td>Robustness</td>
                    <td>{{ scores.robustness }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="tile is-parent is-vertical">
            <div
              class="tile is-child is-justify-content-center"
              style="display: flex"
            >
              <!-- <figure class="image is-1by1"> -->
              <!-- <figure class="image"> -->
              <!-- <img
                class="has-ratio"
                width="256"
                height="256"
                src="../assets/picNotFound.svg"
              /> -->
              <!-- </figure> -->
              <div
                id="radar"
                ref="mychart"
                style="height: 300px; width: 400px"
              ></div>
            </div>
            <div class="tile is-child">
              <p class="has-text-centered">
                <i class="fa fa-hand-o-right mr-3 has-text-primary"></i
                >您的测试结果反映出该系统的<b>易用性</b>和<b>健壮性</b>有待提升！<br />
              </p>
            </div>
            <div class="tile is-child has-text-centered">
              <!-- has-text-centered 中对 button 也有效 -->
              <button class="button is-primary" style="margin: 0 20px">
                <i class="fa fa-download mr-3"></i>导出详细结果
              </button>
              <p class="has-text-grey is-size-7">
                导出详细眼动指标、眼动追踪图像
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <footer class="footer pt-4 pb-6">
      <div class="content has-text-centered">
        All rights reserved by BJUT RELab.
      </div>
    </footer>
  </div>
</template>

<script>
import * as echarts from "echarts";
import axios from "axios";

export default {
  data() {
    return {
      scores: {
        accessibility: "",
        easeOfUse: "",
        consistency: "",
        accuracy: "",
        deviceEfficiency: "",
        robustness: "",
      },
    };
  },
  methods: {
    createChart() {
      const option = {
        radar: {
          shape: "circle",
          radius: 100,
          indicator: [
            { name: "Accessibility", max: 100 },
            { name: "Ease of use", max: 100 },
            { name: "Consistency", max: 100 },
            { name: "Accuracy", max: 100 },
            { name: "Device efficiency", max: 100 },
            { name: "Robustness", max: 100 },
          ],
          axisName: {
            color: "#4a4a4a",
          },
        },
        series: [
          {
            name: "Budget vs spending",
            type: "radar",
            data: [
              {
                value: [
                  this.scores.accessibility,
                  this.scores.easeOfUse,
                  this.scores.consistency,
                  this.scores.accuracy,
                  this.scores.deviceEfficiency,
                  this.scores.robustness,
                ],
                name: "Allocated Budget",
                areaStyle: {
                  // color: "hsl(171, 100%, 41%)",
                  // color: "rgb(0, 209, 178)",
                  // color: "#00d1b2",
                  // 以上三种方式都可以（bulma 的 primary color）
                  color: "hsl(171, 100%, 41%)",
                },
              },
            ],
          },
        ],
      };
      const myChart = echarts.init(this.$refs.mychart);
      // const myChart = echarts.init(document.getElementById("radar"));
      myChart.setOption(option);
    },
  },
  mounted() {
    axios.get("/api/get_scores").then((response) => {
      this.scores = response.data.scores;
      this.createChart();
    });
  },
};
</script>

<style></style>
