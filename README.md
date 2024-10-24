### Steps

1. Clone the repository:

```bash
git clone
cd RAG
```

2. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run the FastAPI server:

```bash
uvicorn main:app --reload
```

5. Run the Streamlit app in another terminal:

```bash
streamlit run app.py
```
