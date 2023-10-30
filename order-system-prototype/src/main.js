import { createApp } from "vue";
import App from "./App.vue";
import installElementPlus from "./plugins/element";
import router from "./router";
import axios from "axios";
import "bulma/css/bulma.css";
import "font-awesome/css/font-awesome.css";

const app = createApp(App);
app.config.globalProperties.axios = axios;
app.config.globalProperties.$Accessibility = false;
// app.config.globalProperties.$Accessibility = true
app.config.globalProperties.$Ease_of_use = false;
// app.config.globalProperties.$Ease_of_use = true
app.config.globalProperties.$Accuracy = false;
// app.config.globalProperties.$Accuracy = true
app.config.globalProperties.$Consistency = false;
// app.config.globalProperties.$Consistency = true
app.config.globalProperties.$Device_efficiency = false;
// app.config.globalProperties.$Device_efficiency = true
// app.config.globalProperties.$Robustness = false
app.config.globalProperties.$Robustness = true;
installElementPlus(app);
app.use(router).mount("#app");
