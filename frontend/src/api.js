export async function postJsonForPdf(data) {
  const res = await fetch('/api/generate-pdf', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || 'Failed to generate PDF')
  }
  return await res.blob()
}

export async function postFileForPdf(file) {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch('/api/generate-pdf', { method: 'POST', body: form })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || 'Failed to generate PDF')
  }
  return await res.blob()
}
