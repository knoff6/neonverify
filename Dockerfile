FROM python:3.9-slim

# Install system dependencies
# gcc: for compiling the privesc binary
# netcat: for debugging/testing (optional but good for CTF)
RUN apt-get update && apt-get install -y \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Setup Flags
# User flag in a typical user location (simulated)
RUN useradd -m -s /bin/bash neon
COPY flags/user.txt /home/neon/user.txt
RUN chown neon:neon /home/neon/user.txt && chmod 644 /home/neon/user.txt

# Root flag
COPY flags/root.txt /root/root.txt
RUN chmod 600 /root/root.txt

# Setup Privilege Escalation
# Compile the binary
RUN gcc privesc/verifier.c -o /usr/local/bin/neon-check

# Set SUID bit (Critical for the exploit)
RUN chown root:root /usr/local/bin/neon-check && chmod 4755 /usr/local/bin/neon-check

# Create the dummy log file needed for the binary
RUN touch /var/log/neon_verify.log && chmod 644 /var/log/neon_verify.log

# Setup Database
RUN python setup_db.py

# Expose port
EXPOSE 5000

# Run the application
# We run as root because the SUID exploit needs to escalate TO root.
# In a real scenario, the web app should run as a low-priv user (e.g., www-data),
# and the attacker exploits that to get a shell as www-data, then uses the SUID binary to get root.
# Let's try to simulate that better.

# Create a low privilege user for the web app
RUN useradd -m -s /bin/bash webuser
RUN chown -R webuser:webuser /app

# Switch to low privilege user
USER webuser

# Command to run the app
CMD ["python", "app.py"]
