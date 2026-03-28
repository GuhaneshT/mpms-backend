# M-PMS Backend API

This is the FastAPI backend for the Machine Management Property Management System (M-PMS). It handles machine data, service call logging, advanced reliability querying, and interacts directly with Supabase via PostgreSQL and SQLAlchemy.

## Tech Stack
*   **Framework:** FastAPI (Python 3.10+)
*   **Database:** PostgreSQL (Hosted on Supabase)
*   **ORM:** SQLAlchemy
*   **Data Validation:** Pydantic
*   **Authentication:** Supabase JWT Verification

## API Structure
*   **`/api/v1/machines`**: CRUD operations and status updates for machines.
*   **`/api/v1/service-calls`**: Logging and tracking diagnostic service calls.
*   **`/api/v1/dashboard`**: Aggregated reliability metrics (MTBF, MTTR, Traffic Light system).
*   **`/api/v1/users`**: Technician profile matching.

## Local Setup

1.  **Clone the repository (if split):**
    ```bash
    git clone https://github.com/GuhaneshT/mpms-backend.git
    cd mpms-backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root of the `backend` directory:
    ```env
    DATABASE_URL=postgresql://postgres.your_project:[YOUR-PASSWORD]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
    SUPABASE_URL=your_supabase_project_url
    SUPABASE_KEY=your_supabase_service_role_key
    FRONTEND_URL=http://localhost:5173 # Update this to your Vercel URL in production
    ```

5.  **Run the development server:**
    ```bash
    uvicorn main:app --reload --port 8000
    ```
    The API documentation will be available at `http://localhost:8000/docs`.

## Deployment
This FastAPI backend is structured perfectly to be deployed as a **Web Service** on [Render.com](https://render.com). 
* Build Command: `pip install -r requirements.txt`
* Start Command: `uvicorn main:app --host 0.0.0.0 --port 10000`
