const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function uploadDocument(file: File) {
    // Send a POST request to the backend endpoint defined
    // in ./backend/app/routers/documents.py

    // Send the file using FormData instead of JSON.
    // The backend expects the uploaded file under the field name "file",
    //  > [file: UploadFile = File(...)] in upload_document definition.
    // So the FormData field name must be "file".
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/documents/upload`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error(await response.text());
    }

    // Parse and return the JSON response that matches DocumentResponse like below:
    // {
    //     "id": 1,
    //     "filename": "example.txt",
    // }
    return response.json();
}

export async function queryDocuments(question: string, accessCode: string) {
     // Send a POST request to the backend endpoint defined
     // in ./backend/app/routers/query.py

     // The request body must match the backend QueryRequest schema in ./backend/app/schemas.py
     // Set body to right schema in this (question and access_code).
    const response = await fetch(`${API_BASE_URL}/query`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            question,
            access_code: accessCode,
        }),
    });

    if (!response.ok) {
        throw new Error(await response.text());
    }

    // Also returns "QueryResponse" returned from python.
    return response.json();
}