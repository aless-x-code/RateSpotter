from config import app
import os



# make sure that new reviews are synchronized correctly
# deploy to google cloud + github
# market the service (price?)
# Go over all (clean code)
    # go over mongo db documnetation
    # Efficiency? ChatGTP paste all
    # improve library function parameters
    # remove type:ignore
# Test many restaurants and interaction (test py as well)
# Fix CSS
    # @media css
    # too long username, dropdown reviews
# Add more reviews (5)
# Input validation

# Git tracker
# input validation







if __name__ == "__main__":
    app.run(host="0.0.0.0", 
            debug=True, # debug False
            port=int(os.environ.get("PORT", 8080)))
