# Import the create_app function from the 'app' module
from app import create_app

# Create the Flask app using the factory function
app = create_app()

# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True)