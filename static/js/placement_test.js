let appState = {
    index: 0,
    score: 0,
    wrong: 0,
    seconds: 0,
    name: "",
    answered: false
};


function startApp() {
    const nameInput = document.getElementById("user-name");
    if (!nameInput.value.trim()) return alert("لطفا نام خود را وارد کنید");

    appState.name = nameInput.value;

    // fetch questions from server right before starting the test
    let url = window.CONFIG.QUESTIONS_URL;
    fetch(url)
        .then(r => r.json())
        .then(data => {
            window.CONFIG.QUESTIONS = data.questions || [];
            // update duration from server response (seconds); default already set
            if (data.duration_seconds) {
                window.CONFIG.DURATION = data.duration_seconds;
            }

            if (window.CONFIG.QUESTIONS.length === 0) {
                return alert("فعلاً سوالی برای نمایش وجود ندارد.");
            }

            // now reveal the quiz
            document.getElementById("intro-screen").style.display = "none";
            document.getElementById("quiz-screen").style.display = "block";

            // شروع تایمر
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
            // after finishing we will check pass criteria inside finishApp
        })
        .catch(err => {
            console.error("failed to load questions", err);
            alert("خطا در بارگذاری سوال‌ها، لطفاً صفحه را رفرش کنید.");
        });
}
function renderNext() {
    const questions = window.CONFIG.QUESTIONS;
    if (appState.index >= questions.length) return finishApp();

    // آپدیت شمارنده و نوار پیشرفت
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

    // غیرفعال کردن بقیه دکمه‌ها
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

    // no course-specific pass/fail message for global test

    // ارسال به دیتابیس
    fetch(window.CONFIG.SAVE_URL, {
        method: "POST",
        headers: {"X-CSRFToken": window.CONFIG.CSRF_TOKEN, "Content-Type": "application/json"},
        body: JSON.stringify({
            name: appState.name,
            score: appState.score,
            total: total,
            level: level,
            time_seconds: appState.seconds
        })
    });
}