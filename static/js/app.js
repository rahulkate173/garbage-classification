const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const previewImg = document.getElementById('previewImg');
const resultBox = document.getElementById('result');
const labelEl = document.getElementById('label');
const confEl = document.getElementById('conf');
const errorEl = document.getElementById('error');

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (!file) return;
  const url = URL.createObjectURL(file);
  previewImg.src = url;
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  resultBox.classList.add('hidden');
  errorEl.classList.add('hidden');

  const file = fileInput.files[0];
  if (!file) {
    errorEl.textContent = 'Please select an image.';
    errorEl.classList.remove('hidden');
    return;
  }

  const fd = new FormData();
  fd.append('file', file);

  try {
    const res = await fetch('/predict', { method: 'POST', body: fd });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Unknown error');
    labelEl.textContent = data.label ?? '—';
    confEl.textContent = data.confidence ? (data.confidence * 100).toFixed(1) + '%' : '—';
    resultBox.classList.remove('hidden');
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.classList.remove('hidden');
  }
});
