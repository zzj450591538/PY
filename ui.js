// extensions/sd-folder-download/javascript/ui.js
function initDownloadButton() {
    gradioApp().querySelector('#download_btn').addEventListener('click', () => {
        fetch('/sdapi/v1/folder-download', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'outputs.zip';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        });
    });
}

document.addEventListener('DOMContentLoaded', initDownloadButton);
