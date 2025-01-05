Web Light Novel to Ereader Converter
A platform that converts light novels from 1stkissnovel.org into reader-friendly formats like EPUB or PDF, enabling users to enjoy their favorite web novels offline on their preferred e-reading devices.

Features
Convert Light Novels: Seamlessly convert chapters into EPUB or PDF formats.
Offline Reading: Enjoy novels offline on e-readers like Kindle or mobile devices.
Temporary Hosting: Hosted using Ngrok, providing unique temporary links for each session.
How It Works
Input the URL of the novel from 1stkissnovel.org.
Select the desired chapters and output format (EPUB or PDF).
Download the generated file via a temporary link provided by Ngrok.
Setup and Usage
1. Prerequisites
Python: Make sure Python 3.7 or higher is installed.
Ngrok: Download and configure Ngrok.
Dependencies: Install required Python packages.
2. Installation
Clone this repository:

bash
Copy code
git clone https://github.com/ProdiptoPantho/Novel2Reader.git
cd Novel2Reader
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up Ngrok:

bash
Copy code
ngrok config add-authtoken YOUR_AUTH_TOKEN
3. Running the Application
Start the Flask application:

bash
Copy code
python app.py
Start Ngrok to expose the app online:

bash
Copy code
ngrok http 5000
Copy the Ngrok forwarding URL (e.g., https://abcd1234.ngrok.io) and access the app through the browser.

Screenshots
Include screenshots of the interface and an example of an EPUB or PDF conversion.

Limitations
Ephemeral Hosting: Links change with every session as they rely on Ngrok's free service.
1stkissnovel.org Only: Currently supports novel conversion exclusively from this site.
Contributing
Fork the repository.
Create a new branch:
bash
Copy code
git checkout -b feature-branch
Make your changes and commit:
bash
Copy code
git commit -m "Add feature"
Push to your branch and submit a pull request.
License
This project is licensed under the MIT License.
