function getSummary() {
    const youtubeUrl = document.getElementById("youtubeUrl").value;
    const videoId = youtubeUrl.split("=")[1];

    if (!videoId) {
        alert("Please enter a valid YouTube URL.");
        return;
    }

    document.getElementById("thumbnail").innerHTML = `<img src="http://img.youtube.com/vi/${videoId}/0.jpg">`;

    fetch("http://127.0.0.1:5000/summarize", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ youtube_url: youtubeUrl })
    })
    .then(response => response.json())
    .then(data => {
        if (data.summary) {
            document.getElementById("summary").innerText = data.summary;
        } else {
            document.getElementById("summary").innerText = "Error: " + data.error;
        }
    })
    .catch(error => {
        document.getElementById("summary").innerText = "Error fetching summary.";
        console.error("Error:", error);
    });
}
