document.addEventListener("DOMContentLoaded", function () {
  const submitButton = document.getElementById("submitButton");
  const responseDiv = document.getElementById("response");
  const fileInput = document.getElementById("fileInput");
  const dropZone = document.getElementById("dropZone");
  const imagePreview = document.getElementById("imagePreview");

  let selectedFile = null;

  function handleFile(file) {
    if (file && file.type.startsWith("image/")) {
      selectedFile = file;
      previewImage(file);
      responseDiv.textContent = "";
    } else {
      selectedFile = null;
      previewImage(null);
      responseDiv.textContent = "Please select a valid image file (JPEG or PNG).";
    }
  }

  fileInput.addEventListener("change", function (event) {
    if (event.target.files.length > 0) {
      handleFile(event.target.files[0]);
    } else {
      handleFile(null);
    }
  });

  dropZone.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropZone.classList.add("drag-over");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("drag-over");
  });

  dropZone.addEventListener("drop", (event) => {
    event.preventDefault();
    dropZone.classList.remove("drag-over");

    if (event.dataTransfer.files.length > 0) {
      handleFile(event.dataTransfer.files[0]);
    } else {
      handleFile(null);
    }
  });

  function previewImage(file) {
    imagePreview.innerHTML = "";

    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        const img = document.createElement("img");
        img.src = e.target.result;
        img.classList.add("uploaded-image-preview");
        imagePreview.appendChild(img);
      };
      reader.readAsDataURL(file);
    }
  }

  submitButton.addEventListener("click", async function () {
    if (!selectedFile) {
      responseDiv.textContent = "Please select an image first.";
      return;
    }

    if (!selectedFile.type.startsWith("image/")) {
      responseDiv.textContent =
        "Please select a valid image file (JPEG or PNG).";
      return;
    }

    try {
      responseDiv.textContent = "Generating caption...";

      const reader = new FileReader();
      reader.onload = async function (event) {
        try {
          const response = await fetch("/caption/", {
            method: "POST",
            headers: {
              "Content-Type": "application/octet-stream",
            },
            body: event.target.result,
          });

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          const caption = await response.text();
          responseDiv.textContent = `Generated caption: ${caption}`;
        } catch (error) {
          console.error("Error:", error);
          responseDiv.textContent = `Error generating caption: ${error.message}`;
        }
      };
      reader.readAsArrayBuffer(selectedFile);
    } catch (error) {
      console.error("Error:", error);
      responseDiv.textContent = `Error generating caption: ${error.message}`;
    }
  });
});
