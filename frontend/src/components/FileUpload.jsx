import React, { useRef } from 'react'

export default function FileUpload({ accept, onFileSelected }) {
  const inputRef = useRef(null)

  const onChange = (e) => {
    const file = e.target.files?.[0]
    if (file) onFileSelected(file)
  }

  return (
    <div>
      <input ref={inputRef} type="file" accept={accept} onChange={onChange} />
    </div>
  )
}
