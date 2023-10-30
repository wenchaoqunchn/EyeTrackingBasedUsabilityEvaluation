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
      <!-- 如果是 container 就会和 navbar 紧紧贴在一起-->
      <div class="columns">
        <div class="column">
          <div id="upload" class="box my-box">
            <div class="level">
              <div class="level-left">
                <div class="level-item">
                  <p>
                    <!-- <strong><span class="has-text-primary">Step 1</span></strong> -->
                    <span
                      class="has-text-primary has-text-weight-bold is-size-2 m-5"
                      >Step 1</span
                    >
                    <span class="is-size-3">导入待测试系统信息</span>
                  </p>
                </div>
              </div>
            </div>

            <div class="level">
              <div class="level-left">
                <div class="level-item">
                  <div class="content">
                    <p>&emsp;测试前请注意：</p>
                    <ul>
                      <li>请确保眼动仪正确放置并成功连接到电脑；</li>
                      <li>请保持坐姿端正，摘除可能遮挡视线的物品</li>
                      <li>请明确即将在案例系统中执行的用户任务</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <div class="level" style="margin-top: auto">
              <div class="level-item">
                <div class="content">
                  <p  v-if="done"  class="has-text-centered">
                    <i class="fa fa-check-circle has-text-primary mr-3"></i
                    >
                    待测试系统导入成功！
                  </p>
                  <p v-if="done" class="has-text-grey is-size-7 has-text-centered">
                    共导入 23 个 AOI，32 个无关 AOI，1 条扫描路径
                  </p>
                </div>
              </div>
            </div>

            <div class="level" style="margin-top: auto">
              <div class="level-item">
                <el-upload multiple v-on:change="show">
                  <button class="button is-primary">
                    <i  class="fa fa-upload mr-3"></i>点击上传
                  </button>
                  <!-- <template #tip>
                    <div class="el-upload__tip">一些提示信息...</div>
                  </template> -->
                </el-upload>
              </div>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="box my-box">
            <div class="level">
              <div class="level-left">
                <div class="level-item">
                  <p>
                    <!-- <strong><span class="has-text-primary">Step 1</span></strong> -->
                    <span
                      class="has-text-primary has-text-weight-bold is-size-2 m-5"
                      >Step 2</span
                    >
                    <span class="is-size-3">开始测试</span>
                  </p>
                </div>
              </div>
            </div>

            <div class="level">
              <div class="level-left">
                <div class="level-item">
                  <div class="content">
                    <p>&emsp;可用性测试维度：</p>
                    <ul>
                      <li>
                        Accessibility:
                        无论用户的能力如何，都能正常使用软件功能并达成目标；
                      </li>
                      <li>Ease of use: 用户在操作时的难易程度；</li>
                      <li>
                        Consistency: 软件的不同部分的设计语言与规范的一致程度；
                      </li>
                      <li>Accuracy: 软件所提供结果的精确程度；</li>
                      <li>
                        Device efficiency:
                        在使用一定数量的资源时，服务的迅速程度；
                      </li>
                      <li>
                        Robustness:
                        即使在错误的输入下，软件依然能够正常运行的能力。
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <div class="level" style="margin-top: auto">
              <div class="level-item">
                <div class="button is-primary" @click="onClick">
                  <i class="fa fa-play-circle mr-3"></i>开始
                </div>
              </div>
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
import axios from "axios";
import { getCurrentInstance } from "vue";

export default {
  setup() {
    const { proxy } = getCurrentInstance();
    return {
      proxy,
    };
  },
  data() {
    return {
      done: false
    }
  },
  methods: {
    show() {
      this.done = true;
    },
    onClick() {
      axios
        .post("/api/start_record", {
          unix_timestamp: Math.floor(Date.now()),
          Accessibility: this.proxy.$Accessibility,
          Ease_of_use: this.proxy.$Ease_of_use,
          Accuracy: this.proxy.$Accuracy,
          Consistency: this.proxy.$Consistency,
          Device_efficiency: this.proxy.$Device_efficiency,
          Robustness: this.proxy.$Robustness,
        })
        .then((response) => {
          console.log(response);
        });
      this.$router.push("/expr/MyHome/News");
    },
  },
};

</script>

<style>
.my-box {
  height: 100%;
  display: flex;
  flex-direction: column;
  /* 也可以使用 `is-flex-direction-column` 类 */
}
</style>
