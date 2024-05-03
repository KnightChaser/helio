document.getElementById('todoForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;

    fetch('http://127.0.0.1:8080/todos/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: title,
            description: description
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        alert('Todo created successfully!');
        addTodoToTable(data);  // Add the newly created todo to the table
        document.getElementById('todoForm').reset();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to create todo');
    });
});

function fetchTodos() {
    fetch('http://127.0.0.1:8080/todos/')
    .then(response => response.json())
    .then(todos => {
        todos.forEach(todo => {
            addTodoToTable(todo);
        });
    })
    .catch(error => console.error('Error:', error));
}

function addTodoToTable(todo) {
    const tableBody = document.getElementById('todoTable').getElementsByTagName('tbody')[0];
    const row = tableBody.insertRow();
    const cellId = row.insertCell(0);
    const cellTitle = row.insertCell(1);
    const cellDescription = row.insertCell(2);

    cellId.textContent = todo.id;
    cellTitle.textContent = todo.title;
    cellDescription.textContent = todo.description;
}

window.onload = fetchTodos;