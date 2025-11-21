# NeonVerify CTF Challenge

**NeonVerify** is a Cyberpunk-themed "Boot-to-Root" CTF challenge.
**Difficulty**: Beginner/Intermediate
**Objective**: Gain root access and capture the flags (`user.txt` and `root.txt`).

## 🚩 Vulnerabilities
1.  **SQL Injection**: Bypass authentication.
2.  **Remote Code Execution (RCE)**: Unrestricted file upload.
3.  **Privilege Escalation**: SUID binary exploitation (Path Hijacking).

---

## 🚀 Quick Start (Docker) - Recommended
The easiest way to run the challenge is using Docker. This ensures the environment (including the privilege escalation vector) is set up correctly.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/NeonVerify.git
    cd NeonVerify
    ```

2.  **Build the Docker image**:
    ```bash
    docker build -t neonverify .
    ```

3.  **Run the container**:
    ```bash
    docker run -p 5000:5000 -it neonverify
    ```

4.  **Access the CTF**:
    Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 🛠️ Manual Setup (Linux)
If you prefer to run it manually or want to debug the components, follow these steps.
**Note**: The privilege escalation part requires a Linux environment.

### Prerequisites
- Python 3.x
- GCC (for compiling the SUID binary)

### Installation
1.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Initialize the Database**:
    ```bash
    python setup_db.py
    ```

3.  **Setup Privilege Escalation**:
    You need to compile the vulnerable binary and set the SUID bit.
    ```bash
    # Compile the binary
    gcc privesc/verifier.c -o /usr/local/bin/neon-check
    
    # Set ownership and SUID bit (Requires Root)
    sudo chown root:root /usr/local/bin/neon-check
    sudo chmod 4755 /usr/local/bin/neon-check
    
    # Create the dummy log file
    sudo touch /var/log/neon_verify.log
    sudo chmod 644 /var/log/neon_verify.log
    ```

4.  **Run the Application**:
    ```bash
    python app.py
    ```

---

## 🕵️‍♂️ Solution / Walkthrough
**SPOILER ALERT**: The solution is available in [walkthrough.md](walkthrough.md).

## 📂 Project Structure
- `app.py`: The main Flask application.
- `setup_db.py`: Script to initialize the SQLite database.
- `templates/`: HTML templates.
- `static/`: CSS and assets.
- `privesc/`: Source code for the privilege escalation binary.
- `flags/`: Flag files (moved to correct locations during setup).
- `Dockerfile`: Configuration for containerized deployment.

## 📝 License
MIT License - Feel free to use this for educational purposes!
