fetch('/api/notes')
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('notesContainer');
        data.forEach(note => {
            const noteDiv = document.createElement('div');
            noteDiv.innerHTML = `
                <h3>${note.title}</h3>
                <p>${note.content}</p>
                <p>Category: ${note.category}</p>
                <p>Due: ${note.due_date}</p>
            `;
            container.appendChild(noteDiv);
        });
    });
