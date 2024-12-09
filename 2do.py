import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# In-memory list to store todos
todos = []

# HTML templates inline
index_template = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Todo List</title>
  </head>
  <body>
    <h1>Todo List</h1>
    <ul>
      {% for todo in todos %}
        <li>
          <input type="checkbox" {% if todo['done'] %}checked{% endif %} onchange="location.href='{{ url_for('check', index=loop.index0) }}'">
          <span {% if todo['done'] %}style="text-decoration: line-through"{% endif %}>{{ todo['task'] }}</span>
          <a href="{{ url_for('edit', index=loop.index0) }}">edit</a>
          <a href="{{ url_for('delete', index=loop.index0) }}">delete</a>
        </li>
      {% endfor %}
    </ul>
    <form action="{{ url_for('add') }}" method="post">
      <input type="text" name="todo" required>
      <button type="submit">Add</button>
    </form>
  </body>
</html>
"""

edit_template = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Edit Todo</title>
  </head>
  <body>
    <h1>Edit Todo</h1>
    <form action="{{ url_for('edit', index=index) }}" method="post">
      <input type="text" name="todo" value="{{ todo['task'] }}" required>
      <button type="submit">Save</button>
    </form>
  </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(index_template, todos=todos)

@app.route('/add', methods=['POST'])
def add():
    todo = request.form['todo']
    todos.append({'task': todo, 'done': False})
    return redirect(url_for('index'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    todo = todos[index]
    if request.method == 'POST':
        todo['task'] = request.form['todo']
        return redirect(url_for('index'))
    return render_template_string(edit_template, todo=todo, index=index)

@app.route('/check/<int:index>')
def check(index):
    todos[index]['done'] = not todos[index]['done']
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete(index):
    del todos[index]
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Port for Cloud Run compatibility
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
