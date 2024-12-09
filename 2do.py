from flask import Flask, request, redirect, url_for
from flask import render_template_string

app = Flask(__name__)

todos = []

# HTML templates as strings
INDEX_HTML = """
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
          <input type="checkbox" {% if todo['done'] %}checked{% endif %} onclick="location.href='{{ url_for('toggle', index=loop.index0) }}'">
          <span {% if todo['done'] %}style="text-decoration: line-through"{% endif %}>{{ todo['task'] }}</span>
          <a href="{{ url_for('edit', index=loop.index0) }}">edit</a>
          <a href="{{ url_for('delete', index=loop.index0) }}">delete</a>
        </li>
      {% endfor %}
    </ul>
    <form action="{{ url_for('add') }}" method="post">
      <input type="text" name="task" required>
      <button type="submit">Add</button>
    </form>
  </body>
</html>
"""

EDIT_HTML = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Edit Todo</title>
  </head>
  <body>
    <h1>Edit Todo</h1>
    <form action="{{ url_for('edit', index=index) }}" method="post">
      <input type="text" name="task" value="{{ todo['task'] }}" required>
      <button type="submit">Save</button>
    </form>
  </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML, todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    todos.append({'task': task, 'done': False})
    return redirect(url_for('index'))

@app.route('/toggle/<int:index>')
def toggle(index):
    todos[index]['done'] = not todos[index]['done']
    return redirect(url_for('index'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if request.method == 'POST':
        todos[index]['task'] = request.form['task']
        return redirect(url_for('index'))
    return render_template_string(EDIT_HTML, todo=todos[index], index=index)

@app.route('/delete/<int:index>')
def delete(index):
    del todos[index]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
