/* =========================================================
   FAMILY FUTURE FUND
   FRONTEND JAVASCRIPT
========================================================= */


// =========================================================
// UNDERSTAND MY GOAL
// =========================================================

function understandGoal() {

    const goalInput = document.getElementById("goalInput");

    if (!goalInput) {
        return;
    }

    const text = goalInput.value.trim();

    if (text === "") {

        alert("Please describe your future goal.");

        goalInput.focus();

        return;
    }


    // Save user's original goal sentence
    localStorage.setItem(
        "userGoalText",
        text
    );


    // Open NLP Goal Understanding page
    window.location.href = "goal.html";
}