import React, { useState } from 'react'
import JsonEditor from './components/JsonEditor'
import FileUpload from './components/FileUpload'
import { postJsonForPdf, postFileForPdf } from './api'

export default function App() {
  const [jsonData, setJsonData] = useState('')
  const [status, setStatus] = useState('')

  const handleGenerateFromJson = async () => {
    try {
      setStatus('Validating JSON...')
      const parsed = JSON.parse(jsonData)
      setStatus('Generating PDF...')
      const blob = await postJsonForPdf(parsed)
      triggerDownload(blob, 'Striver_Questions.pdf')
      setStatus('PDF downloaded!')
    } catch (e) {
      console.error(e)
      setStatus(`Error: ${e.message}`)
    }
  }

  const handleGenerateFromFile = async (file) => {
    try {
      setStatus('Uploading file and generating PDF...')
      const blob = await postFileForPdf(file)
      triggerDownload(blob, 'Striver_Questions.pdf')
      setStatus('PDF downloaded!')
    } catch (e) {
      console.error(e)
      setStatus(`Error: ${e.message}`)
    }
  }

  const triggerDownload = (blob, filename) => {
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    window.URL.revokeObjectURL(url)
  }

  return (
    <div className="container">
      <h1>DSA PDF Generator</h1>
      <p>Paste or upload a JSON like <code>data.json</code> and generate a PDF.</p>

      {/* <div className="card">
        <h2>Paste JSON</h2>
        <JsonEditor value={jsonData} onChange={setJsonData} />
        <button className="primary" onClick={handleGenerateFromJson}>Generate PDF from JSON</button>
      </div> */}

      <div className="card">
        <h2>Upload JSON File</h2>
        <FileUpload accept="application/json" onFileSelected={handleGenerateFromFile} />
      </div>

      <div className="status">{status}</div>
    </div>
  )
}
