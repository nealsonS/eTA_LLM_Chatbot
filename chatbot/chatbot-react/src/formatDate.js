// src/utils/formatDate.js
export function formatDate(dateString) {
    const options = { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true };
    const date = new Date(dateString);
    return date.toLocaleString('en-US', options);
}
