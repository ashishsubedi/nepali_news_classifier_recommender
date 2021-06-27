const BASE_URL = "http://127.0.0.1:5000";

window.addEventListener("load", async () => {
    document.getElementById("classifier").focus();
    document.getElementById("classifier").click();
});

let recommendationList = [];
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

    // console.log(parsedResData);
    
    // Object.keys(parsedResData.id).map((key, index) => {
    //     console.log("BORRRU",key, index);
    //     // recommendationList[]
    //     // recommendationList.push(parsedResData[key]);
    //     // console.log(recommendationList)
    // });
    Object.keys(parsedResData.id).forEach(id=>{
        console.log(id)
        recommendationList.push({
            id : {
                'text':parsedResData.text[id],
                'class':parsedResData.class[id]
            }
        })
    })
    // console.log(Object.keys(parsedResData.id))

    console.log(recommendationList);
};

const handleClassifierClick = async () => {
    document.getElementById("r-content").style.visibility = "hidden";
    document.getElementById("c-content").style.visibility = "visible";
    document.getElementById("c-result").style.visibility = "visible";
};

const handleClassifierSubmit = async (e) => {
    e.preventDefault();
    const textInput = e.target.children[0].value;

    const res = await fetch(`${BASE_URL}/api/classify`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: textInput }),
    });

    const resData = await res.json();
    document.getElementById("c-result").innerHTML = "Classification: " + resData.message;
};

const handleRecommenderSubmit = () => {
    const id = document.getElementById("recommender-form");
    console.log(id);
};

document.getElementById("classifier").addEventListener("click", handleClassifierClick);
document.getElementById("recommender").addEventListener("click", handleRecommenderClick);
document.getElementById("form").addEventListener("submit", handleClassifierSubmit);
