document.addEventListener("DOMContentLoaded", () => {
  const tasks = document.querySelectorAll(".task-card");
  tasks.forEach((task, index) => {
    task.style.animation = `popIn 0.4s ease ${(index * 0.1).toFixed(1)}s both`;
  });
});

const style = document.createElement("style");
style.innerHTML = `
@keyframes popIn {
  from {opacity: 0; transform: translateY(20px) scale(0.95);}
  to {opacity: 1; transform: translateY(0) scale(1);}
}`;
document.head.appendChild(style);
