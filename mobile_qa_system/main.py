from pathlib import Path
from agents.supervisor import Supervisor

def main():
    print("Mobile QA System starting...")
    base_dir = Path(__file__).parent
    supervisor = Supervisor(base_dir)
    supervisor.start_run()
    print("System ready.")

if __name__ == "__main__":
    main()
