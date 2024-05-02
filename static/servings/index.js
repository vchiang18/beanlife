// alert("index.js hooked up!");

let circularProgress = document.querySelector(".circular-progress");
let progressValue = document.querySelector(".progress-value");
console.log(progressValue);


let progressStartValue = 0,
    progressEndValue = 100,
    speed = 80;

let progress = setInterval( () => {
    progressStartValue++;
    progressValue.textContent = `${progressStartValue}%`
    circularProgress.style.background = `conic-gradient(#eea516 ${progressStartValue *3.6}deg, #E4D6C4 0deg)`

    if(progressStartValue == progressEndValue) {
        clearInterval(progress);
    }
    // console.log(progressStartValue);
}, speed);
