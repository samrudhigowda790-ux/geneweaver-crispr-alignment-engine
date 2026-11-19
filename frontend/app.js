async function runAlignment() {
    const button = document.getElementById("alignButton");
    const message = document.getElementById("message");
    const results = document.getElementById("results");

    const payload = {
        sequence_a: document.getElementById("sequenceA").value.trim(),
        sequence_b: document.getElementById("sequenceB").value.trim(),
        match_score: Number(document.getElementById("match").value),
        mismatch_penalty: Number(document.getElementById("mismatch").value),
        gap_penalty: Number(document.getElementById("gap").value)
    };

    button.disabled = true;
    message.textContent = "";

    try {
        const response = await fetch("/api/align", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Alignment failed");

        document.getElementById("score").textContent = data.alignment_score;
        document.getElementById("mismatchCount").textContent = data.mismatch_positions.length;
        document.getElementById("gapCount").textContent = data.gap_count;
        document.getElementById("alignedA").textContent = data.aligned_sequence_a;
        document.getElementById("alignedB").textContent = data.aligned_sequence_b;
        document.getElementById("positions").textContent =
            "Mismatch positions: " + (data.mismatch_positions.join(", ") || "None");

        results.classList.remove("hidden");
    } catch (error) {
        message.textContent = error.message;
        results.classList.add("hidden");
    } finally {
        button.disabled = false;
    }
}
