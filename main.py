from config import app
import os



if __name__ == "__main__":
    app.run(host="0.0.0.0", 
            debug=False,
            port=int(os.environ.get("PORT", 8080)))
