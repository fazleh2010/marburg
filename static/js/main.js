window.onload = function() {
    fetch('/api/nodes')
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById('people-list');
            data.forEach(name => {
                const li = document.createElement('li');
                li.textContent = name;
                list.appendChild(li);
            });
        });
};
