addTaskBtn = document.querySelector(".add-task-btn");


addTaskBtn.addEventListener('click', () => {
    taskTitle = document.querySelector(".task-title").value;
    taskDescription = document.querySelector(".task-description").value;
    taskPriority = Number(document.querySelector(".task-priority").value);
    taskStatus = document.querySelector(".task-status").value;
    fetch("/add", {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            task_title: taskTitle
        })
    });
});