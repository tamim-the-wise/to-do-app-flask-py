addTaskBtn = document.querySelector(".add-task-btn");


addTaskBtn.addEventListener('click', () => {
    taskTitle = "Do onushiloni 8.3"
    taskDescription = "Do home tutor's math hw"
    parentTaskId = 2
    fetch("/add", {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            // task_title: taskTitle,
            // task_description: taskDescription
            // parent_task_id: parentTaskId
        })
    });
});