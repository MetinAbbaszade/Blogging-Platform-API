from app import create_app, create_db_and_tables
app = create_app()

if __name__ == "__main__":
    import uvicorn

    create_db_and_tables()
    uvicorn.run(app=app, host='0.0.0.0', port=8000)
    