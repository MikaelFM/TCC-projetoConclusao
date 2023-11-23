from app import app
from app import scheduler
from app.functions.email import backup_emails_programados
DEBUG = True

if __name__ == "__main__":
    scheduler.start()
    backup_emails_programados()
    app.run(debug=True)
