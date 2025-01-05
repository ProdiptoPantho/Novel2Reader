# Web Light Novel to Ereader Converter

A platform that converts light novels from [1stkissnovel.org](https://1stkissnovel.org) into reader-friendly formats like **EPUB** or **PDF**, enabling users to enjoy their favorite web novels offline on their preferred e-reading devices.

## Features
- **Convert Light Novels**: Seamlessly convert chapters into **EPUB** or **PDF** formats.
- **Offline Reading**: Enjoy novels offline on e-readers like Kindle or mobile devices.
- **Temporary Hosting**: Hosted using **Ngrok**, providing unique temporary links for each session.

## How It Works
1. Input the URL of the novel from [1stkissnovel.org](https://1stkissnovel.org).
2. Select the desired chapters and output format (EPUB or PDF).
3. Download the generated file via a temporary link provided by Ngrok.

## Setup and Usage

### 1. Prerequisites
- **Python**: Make sure Python 3.7 or higher is installed.
- **Ngrok**: Download and configure [Ngrok](https://ngrok.com/download).
- **Dependencies**: Install required Python packages.

### 2. Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/ProdiptoPantho/Novel2Reader.git
   cd Novel2Reader
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Ngrok:
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN
   ```

### 3. Running the Application
1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Start Ngrok to expose the app online:
   ```bash
   ngrok http 5000
   ```

3. Copy the Ngrok forwarding URL (e.g., `https://abcd1234.ngrok.io`) and access the app through the browser.

## Screenshots
_Include screenshots of the interface and an example of an EPUB or PDF conversion._

## Limitations
- **Ephemeral Hosting**: Links change with every session as they rely on Ngrok's free service.
- **1stkissnovel.org Only**: Currently supports novel conversion exclusively from this site.

## Contributing
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Add feature"
   ```
4. Push to your branch and submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).
