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
   run ```pip install -r requirements.txt```
4. Run app.py using ```python app.py``` 

### YouTube Walkthrough:
Link: https://www.youtube.com/watch?v=MroQUOuldTI

### Running the Application
Website - www.trustsignature.app
or 
1. Start the Flask server
   python app.py
2. Open the UI in your browser
   http://127.0.0.1:5000

Sample Username and Password:
1. Email: test@test.com
2. Password: password

Note that you can also create your own account if you would like, each payment and signature that you add will stay attached to your account.


### Changes since DP4:
We took the feedback from our fellow students and TAs and made modifications to our app.
Note that these changes are discussed in depth with pictures in our DP6 PPTX file.
Most notably these changes include: 
* Spreading out the content horizontally to make more use of the screen real estate.
* Changing from small selection menus to large buttons that display all the data clearly and demonstrates that one must be chosen.
* A larger back button to make traversal clearer.
* Input validation to only allow for the correct inputs that do not throw errors.
* Additionally, there are now options to delete your bank and signatures if you do not want them anymore. They will not be a selectable option, but they will still be visible on past payments.



### UI Work Flow
#### 1. Sign In / Registration
   * Users create an account or log in from main entry page
   * Password are hashed for security
   * On successful login, users are redirected to home / dashboard page

#### 2. Home / Dashboard
   * Displays a welcome message and navigation options
   * View account information
   * Bank link page navigation
   * Manage digital signature and payments

#### 3. Link Bank Account (Simple Task)
   * User enters bank name, account number, routing number
   * Form allows user to add bank account details
   * After submitting, the data is stored in SQLite with success confirmation message
   * Connection between UI, backend, and database
   * User is shown their updated list of connected bank acccounts

#### 4. Manage Digital Signature (Medium Task)

   Step 1 - Update Profile
   * User navigates to Manange Profile
   * They update fields such as name, email, or other basic info
   * Changes are submitted and saved using SQLite

   Step 2 - Manage Signature
   * Users click Manage Trust Signature, entering the signature setup page

   Step 3 - Add Signature
   Users can:
   * Draw a signature (simulated)
   * Upload a signature image

   Step 4 - Encryption & Verfication
   * After choosing a signature, the system shows a simulated encryption process
   * User is shown confirmation screen
   
#### 5. Make a Verified Payment (Hard Task)

   Step 1 - Create Payment
   * User enters recipient information, amount, adds signature and confrims

   Step 2 - Save Payment
   * Information is stored in SQLite database
   * A confirmation messages appears after saving

   Step 3 - View All Payments
   * User navigates to All Payments
   * A table or list show all their past transactions

   Step 4 - Download Receipt
   * User clicks on a payment entry
   * A receipt page opens showing amount, timestamp, and status.
   * User clicks Download to save it as a PDF (if implemented) or view only HTML

### Browser / Device Settings
* Optimized for desktop browsers
* Not yet optimized for mobile or tablet layouts
* JavaScript must be enabled in the browser

### Limitations
* Prototype does not connect real banking APIs
* Some planned features may only be partially implemented depending on project phase
* Error handling and validation are basic. At the moment not a production ready banking system
