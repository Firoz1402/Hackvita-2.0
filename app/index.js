function process() {
    var formData = new FormData(document.getElementById("uploadForm"));

    fetch("http://127.0.0.1:5000/process", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        var resultDiv = document.getElementById("result");
        resultDiv.innerHTML = "";

        if (data.length === 0) {
            resultDiv.innerHTML = "No occurrences found.";
        } else {
            data.forEach(item => {
                resultDiv.innerHTML += `<p>Occurrence: ${item.occurrence}, Start Time: ${item.start_time.toFixed(2)}s, Duration: ${item.duration.toFixed(2)}s</p>`;
            });
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

