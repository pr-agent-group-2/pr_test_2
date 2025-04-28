// Simple client to hydrate HTML after htmx loads server‑rendered JSON
document.addEventListener('htmx:afterSwap', (e) => {
    if (e.target.id === 'todo-list' && e.detail.xhr.responseType === '' ) {
        const todos = JSON.parse(e.detail.xhr.responseText);
        const list = document.getElementById('todo-list');
        list.innerHTML = '';
        const template = document.getElementById('todo-item-template').content;
        todos.forEach(todo => {
            const node = template.cloneNode(true);
            const li = node.querySelector('li');
            li.dataset.id = todo.id;
            if (todo.completed) li.classList.add('completed');
            node.querySelector('input[type=checkbox]').checked = todo.completed;
            node.querySelector('.title').textContent = todo.title;

            node.querySelector('input[type=checkbox]').addEventListener('change', async evt => {
                await fetch(`/todos/${todo.id}`, {
                    method: 'PUT',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({completed: evt.target.checked})
                });
                li.classList.toggle('completed', evt.target.checked);
            });

            node.querySelector('button.delete').addEventListener('click', async () => {
                await fetch(`/todos/${todo.id}`, {method: 'DELETE'});
                li.remove();
            });

            list.appendChild(node);
        });
    }
});

// Intercept new‑todo form submission to send JSON instead of form‑urlencoded
document.getElementById('new-todo-form').addEventListener('submit', async evt => {
    evt.preventDefault();
    const form = evt.target;
    const title = form.title.value.trim();
    if (!title) return;
    const res = await fetch('/todos', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title})
    });
    const todo = await res.json();
    // Reload list
    const list = document.getElementById('todo-list');
    const evtFetch = await fetch('/todos');
    const todos = await evtFetch.json();
    htmx.process(document.body); // to trigger afterSwap manually
    // hack: simulate htmx load
    const fakeEvt = new Event('htmx:afterSwap');
    fakeEvt.target = list;
    fakeEvt.detail = {xhr: {responseText: JSON.stringify(todos), responseType: ''}};
    document.dispatchEvent(fakeEvt);
    form.reset();
});
