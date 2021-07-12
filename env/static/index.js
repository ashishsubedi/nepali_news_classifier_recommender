const BASE_URL = "http://127.0.0.1:5000";

window.addEventListener("load", async () => {
  document.getElementById("classifier").focus();
  document.getElementById("classifier").click();
});

const handleRecommenderClick = async () => {
  document.getElementById("c-content").style.visibility = "hidden";
  document.getElementById("r-content").style.visibility = "visible";
  document.getElementById("c-result").style.visibility = "hidden";

  const res = await fetch(`${BASE_URL}/api/random-news`);
  if (res.status != 200) {
    console.log("Error connecting to the server");
    return;
  }

  const resData = await res.json();
  const parsedResData = JSON.parse(resData.data);

  let recommendationList = [];
  // Object.keys(parsedResData.id).forEach(id=>console.log(id))

  Object.keys(parsedResData.id).forEach((id) => {
    // console.log(id)
    // let d = {}
    // d[id] = {
    //     text: parsedResData.text[id],
    //     class: parsedResData.class[id],
    // }
    recommendationList.push({
      id,
      text: parsedResData.text[id],
      class: parsedResData.class[id],
    });

  });
//   console.log(recommendationList);
  recommendationList.map((item, index) => {
    if (index <= 10) {
      const content =
        `<strong id=${item.id}>Category: ${item.class}</strong> <br><br>` +
        item.text;
      document.getElementById(`${index + 1}`).children[0].innerHTML = content;
      return;
    }
  });
};

const handleClassifierClick = async () => {
  document.getElementById("r-content").style.visibility = "hidden";
  document.getElementById("c-content").style.visibility = "visible";
  document.getElementById("c-result").style.visibility = "visible";
};

const handleClassifierSubmit = async (e) => {
  e.preventDefault();
  document
    .getElementById("c-result")
    .scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });

  const textInput = e.target.children[0].value;

  const res = await fetch(`${BASE_URL}/api/classify`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: textInput }),
  });

  const resData = await res.json();
  document.getElementById("c-result").innerHTML =
    "Classification: " + resData.message;
};

const genTableData = (num, item) => {
  let table = document.getElementById("rt");

  table.innerHTML = `<div class="result-header">Category</div>
    <div class="result-header">News</div>
    <div class="result-header">Score</div>`;

  for (let i = 0; i < item.length; i++) {
    table.innerHTML += `<div class="result" id="category">${item[i][2]}</div>
        <div class="result" id="news">${item[i][1]}</div>
        <div class="result" id="score">${item[i][0]}</div>`;
  }
};

const handleRecommenderSubmit = async (e) => {
  e.preventDefault();
  e.target.style.whiteSpace = "normal";
  document
    .getElementById("rt")
    .scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    console.log(e.target)
  const id = e.target.parentNode.children[0].children[0].getAttribute("id");
  console.log(id)
  const res = await fetch(`${BASE_URL}/api/recommend`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id,
      num: 10,
    }),
  });

  const resData = await res.json();
  const parsedResData = JSON.parse(resData.message);
  genTableData(10, parsedResData);
};

const handleLinkPressed = (e) => {
  e.preventDefault();
  e.target.style.whiteSpace = "normal";
};

document
  .getElementById("classifier")
  .addEventListener("click", handleClassifierClick);
document
  .getElementById("recommender")
  .addEventListener("click", handleRecommenderClick);
document
  .getElementById("form")
  .addEventListener("submit", handleClassifierSubmit);

document.querySelectorAll("#link").forEach((e) => {
  e.addEventListener("click", handleLinkPressed);
});
document.querySelectorAll("#r-btn").forEach((e) => {
  e.addEventListener("click", handleRecommenderSubmit);
});

// document.querySelectorAll("#link").forEach((e) => {
//     e.addEventListener("click", handleRecommenderSubmit);
// });
