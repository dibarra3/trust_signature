# trust_signature

## Description
Trust Signature is a desktop-focused web application that helps user feel more confident about online financial activity.
* Create an account and sign in securely.
* Link bank accounts to their profile
* Add a digital signature and use it to verify payments and generate receipts.

### Requirements 
To run the UI locally, you must:
1. Have **Python** installed version 3.x or higher
2. **pip** Python package manager to install package dependencies
3. A modern desktop browser
* Optional: A virtual environment for isolating project dependencies

### Installation & Setup
1. Clone the repository
2. (If installed) Create and activate virtual environment
3. Install Python dependencies
4. (If needed) Initialize the database

### Running the Application
Website - www.trustsignature.app
or 
1. Start the Flask server
   python app.py
2. Open the UI in your browser
   http://127.0.0.1:5000

### UI Work Flow
1. Sign In / Registration
   * Users create an account or log in from main entry page
   * Password are hashed for security
   * On successful login, users are redirected to home / dashboard page
2. Home / Dashboard
   * Displays a welcome message and navigation options
   * View account information
   * Bank link page navigation
   * Manage digital signature and payments
3. Link Bank Account (Simple Task)
   * Users can open the **Connect Bank** or similar page
   * Form allows user to add bank account details
   * After submitting, the data is stored in SQLite with success confirmation message
   * Connection between UI, backend, and database
4. Manage Digital Signature (Medium Task)
   * Users will access a **Manage Trust Signature** option from profile
   * They will be able to create or upload a digital signature
   * The system will store this in a secure format and display verfication message
5. Make a Verified Payment (Hard Task)
   * Users will be able to select a recipient, enter an amount, and confirm payment
   * The system will show verfication flow and a final confirmation message
   * A receipt page will display details and allow user to download or view a *verified* transaction record

### Browser / Device Settings
* Optimized for desktop browsers
* Not yet optimized for mobile or tablet layouts
* JavaScript must be enabled in the browser

### Limitations
* Prototype does not connect real banking APIs
* Some planned features may only be partially implemented depending on project phase
* Error handling and validation are basic. At the moment not a production ready banking system
