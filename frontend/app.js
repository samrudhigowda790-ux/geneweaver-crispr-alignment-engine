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

let uploadedSequences = [];

async function uploadFasta() {
    const fileInput = document.getElementById("fastaFile");
    const button = document.getElementById("uploadButton");
    const message = document.getElementById("uploadMessage");
    const preview = document.getElementById("fastaPreview");

    const file = fileInput.files[0];

    if (!file) {
        message.textContent = "Please select a FASTA file first.";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    button.disabled = true;
    message.textContent = "Uploading and parsing...";
    preview.classList.add("hidden");

    try {
        const response = await fetch("/api/fasta", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "FASTA upload failed");
        }

        uploadedSequences = data.sequences;

        populateSequenceSelectors();
        displaySequencePreview();

        document.getElementById("sequenceCount").textContent =
            data.sequence_count + " sequence(s) found in " + data.filename;

        preview.classList.remove("hidden");
        message.textContent = "FASTA file parsed successfully.";

    } catch (error) {
        uploadedSequences = [];
        message.textContent = error.message;
    } finally {
        button.disabled = false;
    }
}


function populateSequenceSelectors() {
    const referenceSelect = document.getElementById("referenceSelect");
    const targetSelect = document.getElementById("targetSelect");

    referenceSelect.replaceChildren();
    targetSelect.replaceChildren();

    uploadedSequences.forEach((record, index) => {
        const referenceOption = document.createElement("option");
        referenceOption.value = index;
        referenceOption.textContent = record.id;
        referenceSelect.appendChild(referenceOption);

        const targetOption = document.createElement("option");
        targetOption.value = index;
        targetOption.textContent = record.id;
        targetSelect.appendChild(targetOption);
    });

    if (uploadedSequences.length > 1) {
        targetSelect.value = "1";
    }
}


function displaySequencePreview() {
    const sequenceList = document.getElementById("sequenceList");
    sequenceList.replaceChildren();

    uploadedSequences.forEach((record) => {
        const card = document.createElement("div");
        card.className = "alignment-card";

        const heading = document.createElement("h3");
        heading.textContent = record.id;

        const description = document.createElement("p");
        description.textContent = record.description;

        const sequence = document.createElement("code");
        sequence.textContent = record.sequence;

        card.append(heading, description, sequence);
        sequenceList.appendChild(card);
    });
}


function useSelectedSequences() {
    const referenceIndex = document.getElementById("referenceSelect").value;
    const targetIndex = document.getElementById("targetSelect").value;
    const message = document.getElementById("uploadMessage");

    if (uploadedSequences.length < 2) {
        message.textContent = "Upload at least two sequences to perform alignment.";
        return;
    }

    if (referenceIndex === targetIndex) {
        message.textContent = "Please select two different sequences.";
        return;
    }

    document.getElementById("sequenceA").value =
        uploadedSequences[Number(referenceIndex)].sequence;

    document.getElementById("sequenceB").value =
        uploadedSequences[Number(targetIndex)].sequence;

    message.textContent = "Selected sequences added to the alignment workspace.";

    document.querySelector(".workspace:not(.upload-workspace)").scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


async function scanPamSites() {
    const sequence = document.getElementById("pamSequence").value.trim();
    const pamPattern = document.getElementById("pamPattern").value.trim();

    const message = document.getElementById("pamMessage");
    const results = document.getElementById("pamResults");
    const count = document.getElementById("pamCount");
    const output = document.getElementById("pamOutput");

    results.classList.add("hidden");
    output.textContent = "";
    count.textContent = "";

    if (!sequence) {
        message.textContent = "Please enter a DNA sequence.";
        return;
    }

    message.textContent = "Scanning DNA sequence...";

    try {
        const response = await fetch("/api/pam", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sequence: sequence,
                pam_pattern: pamPattern
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "PAM detection failed.");
        }

        message.textContent = "PAM scan completed.";
        count.textContent = `Found ${data.site_count} PAM site(s).`;

        output.textContent = JSON.stringify(data.pam_sites, null, 2);
        results.classList.remove("hidden");

    } catch (error) {
        message.textContent = error.message;
    }
}
