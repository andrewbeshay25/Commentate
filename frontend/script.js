const apiBaseUrl = "http://localhost:8000"; // Local Docker-hosted FastAPI URL

// Fetch all comments
async function fetchAllComments() {
    try {
        const response = await fetch(`${apiBaseUrl}/comments/`);
        if (!response.ok) throw new Error("Server error while fetching comments");

        const data = await response.json();

        // Check for empty data
        if (data.length === 0) {
            document.getElementById("comments-display").innerHTML = "<p>No comments found.</p>";
            return;
        }

        displayComments(data, "comments-display", "All Comments");
    } catch (error) {
        console.error("Error fetching comments:", error);
        showError("comments-display", "An error occurred while fetching comments.");
    }
}

// Query comments by filters
async function queryComments(event) {
    event.preventDefault();

    const name = document.getElementById("search-name").value;
    const category = document.getElementById("search-category").value;

    try {
        const params = new URLSearchParams();
        if (name) params.append("name", name);
        if (category) params.append("category", category);

        const response = await fetch(`${apiBaseUrl}/comments/?${params}`);
        if (!response.ok) throw new Error("Server error while querying comments");

        const data = await response.json();

        // Check for empty data
        if (data.length === 0) {
            document.getElementById("query-display").innerHTML = "<p>No comments match your filters.</p>";
            return;
        }

        displayComments(data, "query-display", "Search Results");
    } catch (error) {
        console.error("Error querying comments:", error);
        showError("query-display", "An error occurred while querying comments.");
    }
}


// Add a new comment
async function addComment(event) {
    event.preventDefault();

    const name = document.getElementById("add-name").value;
    const message = document.getElementById("add-message").value;
    const category = document.getElementById("add-category").value;

    const newComment = { name, message, category };

    try {
        const response = await fetch(`${apiBaseUrl}/comments/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newComment),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to add comment");
        }

        const result = await response.json();
        document.getElementById("add-result").innerHTML = `<p>Comment added successfully: <b>${result.comment.comment_message}</b></p>`;
    } catch (error) {
        console.error("Error adding comment:", error);
        showError("add-result", error.message);
    }
}

// Helper function to display comments
function displayComments(comments, displayId, title) {
    const display = document.getElementById(displayId);
    if (!comments.length) {
        display.innerHTML = `<p>No comments found.</p>`;
        return;
    }

    let html = `<h3>${title}</h3><ul>`;
    comments.forEach(comment => {
        html += `
            <li>
                <b>${comment.comment_name}</b>: ${comment.comment_message} (${comment.comment_category})
            </li>`;
    });
    html += "</ul>";

    display.innerHTML = html;
}

// Helper function to show errors
function showError(displayId, message) {
    document.getElementById(displayId).innerHTML = `<p style="color: red;">Error: ${message}</p>`;
}
