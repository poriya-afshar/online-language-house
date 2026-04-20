// let appState = {
//     index: 0,
//     score: 0,
//     wrong: 0,
//     seconds: 0,
//     name: "",
//     phone: "",
//     answered: false
// };
// console.log("appState initialized:", appState);

// function startApp() {
//     console.log("startApp function called");

//     const nameInput = document.getElementById("user-name");
//     const phoneInput = document.getElementById("user-phone");

//     console.log("nameInput element:", nameInput);
//     console.log("phoneInput element:", phoneInput);

//     if (!nameInput) {
//         console.error("nameInput not found!");
//         alert("خطا: فیلد نام پیدا نشد!");
//         return;
//     }

//     if (!phoneInput) {
//         console.error("phoneInput not found!");
//         alert("خطا: فیلد شماره تلفن پیدا نشد!");
//         return;
//     }

//     const nameValue = nameInput.value.trim();
//     let phoneValue = phoneInput.value.trim();

//     console.log("Raw name:", nameValue);
//     console.log("Raw phone:", phoneValue);

//     if (!nameValue) {
//         console.warn("Name is empty");
//         alert("لطفا نام خود را وارد کنید");
//         return;
//     }

//     // Clean phone number (only digits)
//     phoneValue = phoneValue.replace(/[^0-9]/g, '');
//     console.log("Cleaned phone:", phoneValue);

//     if (phoneValue.length < 11 || phoneValue.length > 15) {
//         console.warn("Invalid phone length:", phoneValue.length);
//         alert("شماره تلفن باید بین 11 تا 15 رقم باشد (فقط عدد)");
//         return;
//     }

//     // Store values in appState
//     appState.name = nameValue;
//     appState.phone = phoneValue;
//     console.log("appState after assignment:", appState);

//     // Continue with fetching questions...
//     let url = window.CONFIG.QUESTIONS_URL;
//     console.log("Fetching questions from:", url);

//     fetch(url)
//         .then(r => r.json())
//         .then(data => {
//             console.log("Questions received:", data);
//             window.CONFIG.QUESTIONS = data.questions || [];
//             if (data.duration_seconds) {
//                 window.CONFIG.DURATION = data.duration_seconds;
//             }
//             if (window.CONFIG.QUESTIONS.length === 0) {
//                 return alert("فعلاً سوالی برای نمایش وجود ندارد.");
//             }
//             document.getElementById("intro-screen").style.display = "none";
//             document.getElementById("quiz-screen").style.display = "block";

//             const totalDuration = window.CONFIG.DURATION;
//             const timerInterval = setInterval(() => {
//                 appState.seconds++;
//                 let remaining = totalDuration - appState.seconds;
//                 const m = Math.floor(remaining / 60).toString().padStart(2, '0');
//                 const s = (remaining % 60).toString().padStart(2, '0');
//                 const display = document.getElementById("timer-display");
//                 display.innerText = `${m}:${s}`;
//                 if (remaining <= 60) display.classList.add("warning");
//                 if (remaining <= 0) {
//                     clearInterval(timerInterval);
//                     finishApp();
//                 }
//             }, 1000);
//             renderNext();
//         })
//         .catch(err => {
//             console.error("Failed to load questions:", err);
//             alert("خطا در بارگذاری سوال‌ها، لطفاً صفحه را رفرش کنید.");
//         });
// }

// function renderNext() {
//     console.log("renderNext called, index:", appState.index);
//     const questions = window.CONFIG.QUESTIONS;
//     if (appState.index >= questions.length) return finishApp();

//     document.getElementById("progress-counter").innerText = `${appState.index + 1}/${questions.length}`;
//     document.getElementById("progress-fill").style.width = `${((appState.index) / questions.length) * 100}%`;

//     const q = questions[appState.index];
//     const area = document.getElementById("question-area");
//     const labels = ['A', 'B', 'C', 'D'];

//     area.innerHTML = `
//         <div class="question-card">
//             <div class="question-num">سوال شماره ${appState.index + 1}</div>
//             <div class="question-text">${q.text}</div>
//             <div class="options-grid">
//                 ${q.options.map((opt, i) => `
//                     <button class="option-btn" onclick="checkAns(this, ${opt.is_correct})">
//                         <span class="option-label">${labels[i]}</span>
//                         ${opt.text}
//                     </button>
//                 `).join('')}
//             </div>
//         </div>
//     `;
// }

// function checkAns(btn, isCorrect) {
//     console.log("checkAns called, isCorrect:", isCorrect);
//     if (appState.answered) return;
//     appState.answered = true;

//     if (isCorrect) {
//         appState.score++;
//         btn.classList.add("correct");
//     } else {
//         appState.wrong++;
//         btn.classList.add("wrong");
//     }
//     document.querySelectorAll(".option-btn").forEach(b => b.classList.add("disabled"));
//     setTimeout(() => {
//         appState.index++;
//         appState.answered = false;
//         renderNext();
//     }, 800);
// }

// function finishApp() {
//     console.log("finishApp called");
//     document.getElementById("quiz-screen").style.display = "none";
//     document.getElementById("result-screen").style.display = "block";

//     const total = window.CONFIG.QUESTIONS.length;
//     const percent = (appState.score / total) * 100;

//     let level = "A1";
//     if (percent >= 85) level = "C2";
//     else if (percent >= 68) level = "C1";
//     else if (percent >= 51) level = "B2";
//     else if (percent >= 34) level = "B1";
//     else if (percent >= 17) level = "A2";

//     document.getElementById("final-level").innerText = level;
//     document.getElementById("res-correct").innerText = appState.score;
//     document.getElementById("res-wrong").innerText = appState.wrong;
//     document.getElementById("res-time").innerText = appState.seconds;

//     const payload = {
//         name: appState.name,
//         phone: appState.phone,
//         score: appState.score,
//         total: total,
//         level: level,
//         time_seconds: appState.seconds
//     };
//     console.log("Sending payload to server:", payload);

//     fetch(window.CONFIG.SAVE_URL, {
//         method: "POST",
//         headers: { "X-CSRFToken": window.CONFIG.CSRF_TOKEN, "Content-Type": "application/json" },
//         body: JSON.stringify(payload)
//     })
//         .then(response => response.json())
//         .then(data => {
//             console.log("Server response:", data);
//             if (data.status !== "success") {
//                 console.error("Server returned error:", data.message);
//             }
//         })
//         .catch(err => console.error("Save error:", err));
// }


let appState = {
    index: 0,
    score: 0,
    wrong: 0,
    seconds: 0,
    name: "",
    phone: "",
    answered: false
};

function startApp() {
    const nameInput = document.getElementById("user-name");
    const phoneInput = document.getElementById("user-phone");

    if (!nameInput) {
        alert("خطا: فیلد نام پیدا نشد!");
        return;
    }

    if (!phoneInput) {
        alert("خطا: فیلد شماره تلفن پیدا نشد!");
        return;
    }

    const nameValue = nameInput.value.trim();
    let phoneValue = phoneInput.value.trim();

    if (!nameValue) {
        alert("لطفا نام خود را وارد کنید");
        return;
    }

    phoneValue = phoneValue.replace(/[^0-9]/g, '');
    if (phoneValue.length < 11 || phoneValue.length > 15) {
        alert("شماره تلفن باید بین 11 تا 15 رقم باشد (فقط عدد)");
        return;
    }

    appState.name = nameValue;
    appState.phone = phoneValue;

    let url = window.CONFIG.QUESTIONS_URL;
    fetch(url)
        .then(r => r.json())
        .then(data => {
            window.CONFIG.QUESTIONS = data.questions || [];
            if (data.duration_seconds) {
                window.CONFIG.DURATION = data.duration_seconds;
            }
            if (window.CONFIG.QUESTIONS.length === 0) {
                alert("فعلاً سوالی برای نمایش وجود ندارد.");
                return;
            }
            document.getElementById("intro-screen").style.display = "none";
            document.getElementById("quiz-screen").style.display = "block";

            const totalDuration = window.CONFIG.DURATION;
            const timerInterval = setInterval(() => {
                appState.seconds++;
                let remaining = totalDuration - appState.seconds;
                const m = Math.floor(remaining / 60).toString().padStart(2, '0');
                const s = (remaining % 60).toString().padStart(2, '0');
                const display = document.getElementById("timer-display");
                display.innerText = `${m}:${s}`;
                if (remaining <= 60) display.classList.add("warning");
                if (remaining <= 0) {
                    clearInterval(timerInterval);
                    finishApp();
                }
            }, 1000);
            renderNext();
        })
        .catch(err => {
            alert("خطا در بارگذاری سوال‌ها، لطفاً صفحه را رفرش کنید.");
        });
}

function renderNext() {
    const questions = window.CONFIG.QUESTIONS;
    if (appState.index >= questions.length) return finishApp();

    document.getElementById("progress-counter").innerText = `${appState.index + 1}/${questions.length}`;
    document.getElementById("progress-fill").style.width = `${((appState.index) / questions.length) * 100}%`;

    const q = questions[appState.index];
    const area = document.getElementById("question-area");
    const labels = ['A', 'B', 'C', 'D'];

    area.innerHTML = `
        <div class="question-card">
            <div class="question-num">سوال شماره ${appState.index + 1}</div>
            <div class="question-text">${q.text}</div>
            <div class="options-grid">
                ${q.options.map((opt, i) => `
                    <button class="option-btn" onclick="checkAns(this, ${opt.is_correct})">
                        <span class="option-label">${labels[i]}</span>
                        ${opt.text}
                    </button>
                `).join('')}
            </div>
        </div>
    `;
}

function checkAns(btn, isCorrect) {
    if (appState.answered) return;
    appState.answered = true;

    if (isCorrect) {
        appState.score++;
        btn.classList.add("correct");
    } else {
        appState.wrong++;
        btn.classList.add("wrong");
    }
    document.querySelectorAll(".option-btn").forEach(b => b.classList.add("disabled"));
    setTimeout(() => {
        appState.index++;
        appState.answered = false;
        renderNext();
    }, 800);
}

function finishApp() {
    document.getElementById("quiz-screen").style.display = "none";
    document.getElementById("result-screen").style.display = "block";

    const total = window.CONFIG.QUESTIONS.length;
    const percent = (appState.score / total) * 100;

    let level = "A1";
    if (percent >= 85) level = "C2";
    else if (percent >= 68) level = "C1";
    else if (percent >= 51) level = "B2";
    else if (percent >= 34) level = "B1";
    else if (percent >= 17) level = "A2";

    document.getElementById("final-level").innerText = level;
    document.getElementById("res-correct").innerText = appState.score;
    document.getElementById("res-wrong").innerText = appState.wrong;
    document.getElementById("res-time").innerText = appState.seconds;

    const payload = {
        name: appState.name,
        phone: appState.phone,
        score: appState.score,
        total: total,
        level: level,
        time_seconds: appState.seconds
    };

    fetch(window.CONFIG.SAVE_URL, {
        method: "POST",
        headers: { "X-CSRFToken": window.CONFIG.CSRF_TOKEN, "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            if (data.status !== "success") {
                console.error("Server returned error:", data.message);
            }
        })
        .catch(err => console.error("Save error:", err));
}