from flask import Flask, render_template, redirect, url_for, request
import sqlite3

dbName = "todo.db"

def make_db_connection():
    return sqlite3.connect(f"{dbName}")

def close_db_connection(db):
    db.close()

def check_table_exists(tableName):
    db_con = make_db_connection()
    db_cur = db_con.cursor()
    listOfTables = db_cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}';").fetchall()
    if listOfTables == []:
        close_db_connection(db_con)
        return False
    else:
        close_db_connection(db_con)       
        return True

if (not check_table_exists('tasks')):
    dbCon = make_db_connection()
    dbCur = dbCon.cursor()
    query = """CREATE TABLE tasks (
  task_id INTEGER PRIMARY KEY,
  task_title VARCHAR(255) NOT NULL,
  task_description TEXT,
  due_date TIMESTAMP,
  priority SMALLINT CHECK (priority BETWEEN 1 AND 3) DEFAULT 3,
  status VARCHAR(20) CHECK (status IN ('pending', 'in_progress', 'completed')) DEFAULT 'pending',
  parent_task_id INTEGER REFERENCES tasks(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP WITH TIME ZONE
        );"""
    
    dbCur.execute(query)
    close_db_connection(dbCon)


# def organize_tasks_hierarchically(tasks):
#   """
#   This function takes a list of tasks and organizes them into a nested structure
#   representing the parent-child relationships (hierarchy) for presentation.

#   Args:
#       tasks: A list of dictionaries representing tasks, each containing an "id"
#              and a "parent_id" field (can be None for main tasks).

#   Returns:
#       A nested list or dictionary representing the organized task hierarchy.
#   """
#   organized_tasks = []
#   for task in tasks:
#     # Check if task has a parent (subtask)
#     if task["parent_id"] is None:
#       # Main task, add it to the top level
#       organized_tasks.append(task)
#       organized_tasks.append(organize_subtasks(tasks, task["id"]))
#     # Skip processing subtasks handled recursively below
#   return organized_tasks

# def organize_subtasks(tasks, parent_id):
#   """
#   This helper function recursively finds and organizes subtasks for a given parent task.

#   Args:
#       tasks: A list of dictionaries representing tasks.
#       parent_id: The ID of the parent task for which to find subtasks.

#   Returns:
#       A nested list or dictionary containing the subtasks for the given parent.
#   """
#   subtasks = []
#   for task in tasks:
#     if task["parent_id"] == parent_id:
#       subtasks.append(task)
#       # Recursive call to find subtasks for this subtask
#       subtasks.append(organize_subtasks(tasks, task["id"]))
#   return subtasks if subtasks else None  # Return None if no subtasks found


app = Flask(__name__)

@app.route("/")
def index():
    query = "SELECT * FROM tasks"
    dbCon = make_db_connection()
    dbCur = dbCon.cursor()
    data = dbCur.execute(query).fetchall()
    dbCon.commit()
    close_db_connection(dbCon)
    return render_template("index.html", data=data)

@app.route("/add", methods=['POST'])
def add_task():
    data = request.get_json()
    if data.get('task_title'):
        columns = "task_title"
        placeholders = "?"
        values = (data.get('task_title'),)

    if data.get('task_description'):
        columns += ", task_description"
        placeholders += ", ?"
        values += (data.get('task_description'),)
    
    if data.get('due_date'):
        columns += ", due_date"
        placeholders += ", ?"
        values += (data.get('due_date'),)
    
    if data.get('priority'):
        columns += ", priority"
        placeholders += ", ?"
        values += (data.get('priority'),)

    if data.get('status'):
        columns += ", status"
        placeholders += ", ?"
        values += (data.get('status'),)
    
    if data.get('parent_task_id'):
        columns += ", parent_task_id"
        placeholders += ", ?"
        values += (data.get('parent_task_id'),)
    
    if data.get('is_recurring'):
        columns += ", is_recurring"
        placeholders += ", ?"
        values += (data.get('is_recurring'),)
    
    if data.get('recurring_frequency'):
        columns += ", recurring_frequency"
        placeholders += ", ?"
        values += (data.get('recurring_frequency'),)
            
    if data.get('recurrence_rule'):
        columns += ", recurrence_rule"
        placeholders += ", ?"
        values += (data.get('recurrence_rule'),)
    
    query = f"""
        INSERT INTO tasks ({columns})
        VALUES ({placeholders})
    """
    dbCon = make_db_connection()
    dbCur = dbCon.cursor()
    dbCur.execute(query, values)
    dbCon.commit()
    close_db_connection(dbCon)
    return redirect(url_for('index'))

@app.route("/update", methods=['POST'])
def update_task():
    data = request.get_json()
    query = "UPDATE tasks SET "

    if data.get('task_id'):
        taskId = data.get('task_id')
    
    if data.get('task_title'):
        query += f"task_title = {data.get('task_title')}, "

    if data.get('task_description'):
        query += f"task_description = {data.get('task_description')}, "
    
    if data.get('due_date'):
        query += f"due_date = {data.get('due_date')}, "
    
    if data.get('priority'):
        query += f"priority = {data.get('priority')}, "

    if data.get('status'):
        query += f"status = {data.get('status')}, "
    
    if data.get('parent_task_id'):
        query += f"parent_task_id = {data.get('parent_task_id')}, "

    query = query[:-2] + f"WHERE task_id = {taskId}"
    dbCon = make_db_connection()
    dbCur = dbCon.cursor()
    dbCur.execute(query)
    dbCon.commit()
    close_db_connection(dbCon)
    return redirect(url_for('index'))

@app.route("/remove/<task_id>")
def remove_task(task_id):
    query = f"DELETE FROM tasks WHERE task_id={task_id}"
    dbCon = make_db_connection()
    dbCur = dbCon.cursor()
    dbCur.execute(query)
    dbCon.commit()
    close_db_connection(dbCon)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)