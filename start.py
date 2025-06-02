from app.server import run_server

def main():
    run_server()
    raise SystemExit(0)  # Exit gracefully after the server stops
if __name__ == "__main__":
    main()