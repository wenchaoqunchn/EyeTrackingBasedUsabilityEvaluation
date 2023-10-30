import { createRouter, createWebHashHistory } from "vue-router";
import { nextTick } from "vue";
import axios from "axios";

const routes = [
  {
    path: "/setup",
    name: "Setup",
    component: () => import("../views/Setup.vue"),
  },
  {
    path: "/",
    name: "Ready",
    component: () => import("../views/Setup.vue"),
  },
  {
    path: "/expr",
    name: "Expr",
    component: () => import("../views/expr/Main.vue"),
    children: [
      {
        path: "/expr/MyHome",
        name: "MyHome",
        component: () => import("../views/expr/MyHome.vue"),
        children: [
          {
            path: "/expr/MyHome/News",
            name: "News",
            component: () => import("../views/expr/MyHome/News.vue"),
          },
          {
            path: "/expr/MyHome/Agenda",
            name: "Agenda",
            component: () => import("../views/expr/MyHome/Agenda.vue"),
          },
          {
            path: "/expr/MyHome/More",
            name: "More",
            component: () => import("../views/expr/MyHome/More.vue"),
          },
        ],
      },
      {
        path: "/expr/MyLearning",
        name: "MyLearning",
        component: () => import("../views/expr/MyLearning.vue"),
        children: [
          {
            path: "/expr/MyLearning/Library",
            name: "Library",
            component: () => import("../views/expr/MyLearning/Library.vue"),
          },
          {
            path: "/expr/MyLearning/Booking",
            name: "Booking",
            component: () => import("../views/expr/MyLearning/Booking.vue"),
            redirect: "/expr/MyLearning/Booking/SelectSpace",
            children: [
              {
                path: "/expr/MyLearning/Booking/SelectSpace",
                name: "SelectSpace",
                component: () =>
                  import("../views/expr/MyLearning/Booking/SelectSpace.vue"),
              },
              {
                path: "/expr/MyLearning/Booking/SelectDate",
                name: "SelectDate",
                component: () =>
                  import("../views/expr/MyLearning/Booking/SelectDate.vue"),
              },
              {
                path: "/expr/MyLearning/Booking/SelectDateConsistency",
                name: "SelectDateConsistency",
                component: () =>
                  import(
                    "../views/expr/MyLearning/Booking/SelectDateConsistency.vue"
                  ),
              },
              {
                path: "/expr/MyLearning/Booking/SelectDateEaseOfUse",
                name: "SelectDateEaseOfUse",
                component: () =>
                  import(
                    "../views/expr/MyLearning/Booking/SelectDateEaseOfUse.vue"
                  ),
              },
              {
                path: "/expr/MyLearning/Booking/Confirm",
                name: "Confirm",
                component: () =>
                  import("../views/expr/MyLearning/Booking/Confirm.vue"),
              },
              {
                path: "/expr/MyLearning/Booking/SelectSeat",
                name: "SelectSeat",
                component: () =>
                  import("../views/expr/MyLearning/Booking/SelectSeat.vue"),
              },
              {
                path: "/expr/MyLearning/Booking/SelectSeatRobustness",
                name: "SelectSeatRobustness",
                component: () =>
                  import(
                    "../views/expr/MyLearning/Booking/SelectSeatRobustness.vue"
                  ),
              },
              {
                path: "/expr/MyLearning/Booking/SelectSeatDeviceEfficiency",
                name: "SelectSeatDeviceEfficiency",
                component: () =>
                  import(
                    "../views/expr/MyLearning/Booking/SelectSeatDeviceEfficiency.vue"
                  ),
              },
            ],
          },
          {
            path: "/expr/MyLearning/More",
            name: "More2",
            component: () => import("../views/expr/MyLearning/More2.vue"),
          },
        ],
      },
    ],
  },
  {
    path: "/leave",
    name: "Leave",
    component: () => import("../views/Leave.vue"),
  },
  {
    path: "/results",
    name: "Results",
    component: () => import("../views/Results.vue"),
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

var elementsPosition = {};

function getElementLeft(element) {
  var actualLeft = element.offsetLeft;
  var current = element.offsetParent;

  while (current !== null) {
    actualLeft += current.offsetLeft;
    current = current.offsetParent;
  }

  return actualLeft;
}

function getElementTop(element) {
  var actualTop = element.offsetTop;
  var current = element.offsetParent;

  while (current !== null) {
    actualTop += current.offsetTop;
    current = current.offsetParent;
  }

  return actualTop;
}

function scanChildNode(node, path) {
  node.setAttribute("data-path", path);
  try {
    let left = getElementLeft(node);
    let top = getElementTop(node);
    elementsPosition[path] = {
      x1: left,
      y1: top,
      x2: left + node.offsetWidth,
      y2: top + node.offsetHeight,
    };
  } catch (e) {
    return;
  }

  let childNodes = node.childNodes;
  for (let i = 0; i < childNodes.length; i++) {
    let childPath = path + (path === "" ? "" : ",") + i;
    if (childNodes[i].nodeType === 1) scanChildNode(childNodes[i], childPath);
  }
}

router.afterEach(async () => {
  await nextTick();
  scanChildNode(document.getElementById("app"), "");
  axios.post("/api/get_screenshots", {}).then((response) => {
    console.log(response);
  });
});

// router.afterEach(async (to, from) => {
router.beforeEach(async (to, from) => {
  console.log("from: " + from.fullPath + "\nto: " + to.fullPath);
  await nextTick();
  // sleep(1000)
  console.log("after nextTick");
  elementsPosition = {};
  scanChildNode(document.getElementById("app"), "");
  console.log(elementsPosition);
  // // turn elementsPosition to json
  // let json = JSON.stringify(elementsPosition)

  // // send json to server by ajax with cors
  // let xhr = new XMLHttpRequest()
  // xhr.open('POST', 'http://localhost:5000/get_data', true)
  // xhr.setRequestHeader('Content-Type', 'application/json')
  // xhr.send(json)
  // xhr.onreadystatechange = function(){
  //   if (xhr.readyState === 4 && xhr.status === 200){
  //     console.log(xhr.responseText)
  //   }
  // }

  let time;
  time = Math.floor(Date.now());

  // send json to server by axios with cors
  axios
    .post("/api/get_data", {
      path: from.fullPath,
      elements: elementsPosition,
      unix_timestamp: time,
    })
    .then((response) => {
      console.log(response);
      // alert(response.data.class_name)
      // console.log(response.data)
    });

  return true;
});

// function getNodeByPath(path){
//   let root = document.getElementById('app')
//   let arr = path.split(',')
//   for (let i = 0; i < arr.length; i++){
//     if (root.childNodes[arr[i]] === undefined)
//       return null
//     root = root.childNodes[arr[i]]
//   }
//   return root
// }
// console.log(getNodeByPath("0,0,2,1,0,2,1,2,0,1,1"))

export default router;
