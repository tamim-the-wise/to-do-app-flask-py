addTaskBtn = document.querySelector(".add-task-btn");


addTaskBtn.addEventListener('click', () => {
    taskTitle = "Do Math HW"
    taskDescription = "Do home tutor's math hw"
    dueDate = "06/22/2024"
    parentTaskId = 1
    fetch("/add", {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            task_title: taskTitle,
            task_description: taskDescription,
            due_date: dueDate,
            parent_task_id: parentTaskId
        })
    });
});