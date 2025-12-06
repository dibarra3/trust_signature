function updateProgressBar(progressBar, value) {
  const progressFill = progressBar.querySelector(".progress-fill");
  const progressText = progressBar.querySelector(".progress-text");
  const stages = progressText.dataset.stages
    .split(",")
    .map((stage) => stage.split(":"));

  stages.sort((stageA, stageB) => Number(stageB[0]) - Number(stageA[0]));

  const activeStage =
    stages.find((stage) => value >= Number(stage[0])) ||
    stages[stages.length - 1];

  progressFill.style.width = `${value}%`;
  progressText.textContent = `${activeStage[1]}...`;
}

function signatureDelele(fileInput, deletebtn) {
  fileInput.addEventListener("change", () => {
    if (fileInput.files && fileInput.files.length > 0) {
      deletebtn.style.display = "inline-block";
    } else {
      deletebtn.style.display = "none";
    }
  });

  deletebtn.addEventListener("click", () => {
    fileInput.value = "";
    deletebtn.style.display = "none";
    
    const progress = document.getElementById("myProgressBar");

    if (progress) {
      const fill = progress.querySelector(".progress-fill");
      const text = progress.querySelector(".progress-text");
      if (fill) {
        fill.style.width = "0%";
      }
      if (text) {
        text.textContent = "";
      }

      progress.style.display = "none";
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const sigFileInput = document.getElementById("file");
  const sigDeleteBtn = document.getElementById("sig-btn");

  if (sigFileInput && sigDeleteBtn) {
    signatureDelele(sigFileInput, sigDeleteBtn);
  }

  const progressBar = document.getElementById("myProgressBar");
  if (!progressBar) return;

  progressBar.style.display = "none";

  const fileInput = document.querySelector('input[name="file"]'); 
  const downloadBtn = document.querySelector(".download");        

  function startProgress() {
    progressBar.style.display = "block";

    let value = 0;
    const interval = setInterval(() => {
      value += 5;
      if (value > 100) value = 100;

      updateProgressBar(progressBar, value);

      if (value === 100) {
        clearInterval(interval);
      }
    }, 100);
  }

  if (fileInput) {
    fileInput.addEventListener("change", () => {
      if (!fileInput.files || fileInput.files.length === 0) return;
      startProgress();
    });
  }

  if (downloadBtn) {
    downloadBtn.addEventListener("click", (e) => {
      e.preventDefault();
      startProgress();
    });
  }
});


