# PDF Generator API

This application reads data from `data.json` and generates PDF reports that can be sent over the internet via a REST API.

## Features

- **Data Parsing**: Reads JSON data and extracts specific fields (`question_title`, `editorial_link`, `lc_link`, `difficulty`) from the `sub_steps` array
- **PDF Generation**: Creates formatted PDF reports using ReportLab
- **REST API**: Provides endpoints for generating and downloading PDFs
- **Tracing**: Uses Python's built-in logging module for process monitoring and tracing
- **Web-ready**: PDFs can be easily transmitted over the internet

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Backend (Flask API)
1) Install Python deps (prefer a venv or conda env):
```bash
python3 -m pip install -r requirements.txt
```
2) Start the API server:
```bash
python api.py
```
The server runs at `http://localhost:5000`.

Frontend (React with Vite)
1) Install Node deps:
```bash
cd frontend
npm install
```
2) Start the dev server:
```bash
npm run dev
```
Open the URL shown (usually `http://localhost:5173`). The dev server proxies `/api` to the Flask backend.

## API Endpoints

### GET /
Returns API information and available endpoints.

### GET /data-summary
Returns a summary of the JSON data including:
- Total number of topics
- Difficulty breakdown
- Sample topics

### POST /generate-pdf
Generates a PDF from the data and returns the file path and download URL.

### GET /download-pdf
Downloads the generated PDF file directly.

## Example Usage

### Get Data Summary
```bash
curl http://localhost:5000/data-summary
```

### Generate PDF
```bash
curl -X POST http://localhost:5000/generate-pdf
```

### Download PDF
```bash
curl http://localhost:5000/download-pdf -o report.pdf
```

## Data Structure

The application expects `data.json` to contain an array of objects with the following structure:

```json
[
  {
    "step_no": 1,
    "step_title": "Learn the basics",
    "sub_steps": [
      {
        "sub_step_no": 1,
        "sub_step_title": "Things to Know",
        "topics": [
          {
            "question_title": "User Input / Output",
            "editorial_link": "https://example.com/editorial",
            "lc_link": "https://leetcode.com/problems/example",
            "difficulty": 0
          }
        ]
      }
    ]
  }
]
```

## PDF Output

The generated PDF includes:
- Title and summary
- Organized sections by step and sub-step
- Table format for each topic with:
  - Question title
  - Difficulty level (Easy/Medium/Hard)
  - Editorial link
  - LeetCode link

## Dependencies

- Flask: Web framework for API
- ReportLab: PDF generation
- Python's built-in logging: Process tracing
- Standard Python libraries (json, os, tempfile, io, time)

## Tracing and Logging

The application includes comprehensive tracing using Python's logging module:
- Operation start/stop timing
- Checkpoint logging during long operations
- Progress tracking for large datasets
- Error logging with context

All trace logs are output to the console with timestamps and can be redirected to files if needed.
