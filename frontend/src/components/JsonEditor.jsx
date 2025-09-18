import React from 'react'

export default function JsonEditor({ value, onChange }) {
  return (
    <textarea
      className="json-editor"
      rows={18}
      placeholder="Paste your JSON here..."
      value={value}
      onChange={(e) => onChange(e.target.value)}
      spellCheck={false}
    />
  )
}
