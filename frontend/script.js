const apiBaseUrl = "https://commentate.onrender.com"; // Use your Render URL if deployed

async function fetchAllComments() {
    try {
        const response = await fetch(`${apiBaseUrl}`);
        if (!response.ok) throw new Error("Failed to fetch comments");

        const data = await response.json();

        const comments = data.comments;

        if (!comments || Object.keys(comments).length === 0) {
            document.getElementById("comments-display").innerHTML = "<p>No comments found.</p>";
            return;
        }

        let display = "<h3>All Comments</h3><ul>";
        for (const id in comments) {
            display += `<li><b>${comments[id].name}</b>: ${comments[id].message} (${comments[id].category})</li>`;
        }
        display += "</ul>";

        document.getElementById("comments-display").innerHTML = display;
    } catch (error) {
        console.error("Error fetching comments:", error);
        document.getElementById("comments-display").innerHTML = `<p>Error fetching comments: ${error.message}</p>`;
    }
}



async function queryComments(event) {
    event.preventDefault();
    const name = document.getElementById("name").value;
    const message = document.getElementById("message").value;
    const category = document.getElementById("category").value;

    try {
        // Create the query string
        const params = new URLSearchParams();
        if (name) params.append("name", name);
        if (message) params.append("message", message);
        if (category) params.append("category", category);

        // Construct the full URL
        const url = `${apiBaseUrl}/comments/?${params}`;

        // Fetch data from the API
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch comments");

        const data = await response.json();

        // Handle no results
        if (!data.selection || data.selection.length === 0) {
            document.getElementById("query-display").innerHTML = "<p>No results found for the given parameters.</p>";
            return;
        }

        // Render the results
        let display = `<h3>Results</h3><ul>`;
        data.selection.forEach(comment => {
            display += `<li><b>${comment.name}</b>: ${comment.message} (${comment.category})</li>`;
        });
        display += "</ul>";

        document.getElementById("query-display").innerHTML = display;
    } catch (error) {
        console.error("Error querying comments:", error);
        document.getElementById("query-display").innerHTML = `<p>Error querying comments: ${error.message}</p>`;
    }
}



async function addComment(event) {
    event.preventDefault();
    const id = document.getElementById("id").value;
    const message = document.getElementById("add-message").value;
    const name = document.getElementById("add-name").value;
    const category = document.getElementById("add-category").value;

    const newComment = {
        id: parseInt(id),
        message,
        name,
        category
    };

    try {
        const response = await fetch(`${apiBaseUrl}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newComment)
        });

        if (!response.ok) {
            const error = await response.json();
            document.getElementById("add-result").innerHTML = `<p>Error: ${error.detail}</p>`;
            return;
        }

        const result = await response.json();
        document.getElementById("add-result").innerHTML = `<p>Added: ${JSON.stringify(result.Added)}</p>`;
    } catch (error) {
        console.error("Error adding comment:", error);
        document.getElementById("add-result").innerHTML = `<p>Error adding comment: ${error.message}</p>`;
    }
}
