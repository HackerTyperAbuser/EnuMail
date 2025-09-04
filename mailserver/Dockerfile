# Use a base image with a package manager
FROM debian:bullseye-slim

# Install Postfix, Dovecot, and Supervisor
RUN apt-get update && apt-get install -y \
    postfix \
    dovecot-core \
    dovecot-pop3d \
    dovecot-imapd \
    dovecot-lmtpd \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

RUN postconf -e "myhostname = mail.local"
RUN postconf -e "inet_interfaces = all"
RUN postconf -e "mydestination = \$myhostname, localhost"
RUN postconf -e "home_mailbox = Maildir/"

# Copy configuration files (you must create these on your host)
COPY dovecot.conf /etc/dovecot/dovecot.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create a shared directory for mailboxes
RUN mkdir -p /var/mail && chmod 1777 /var/mail

# Expose the necessary ports
EXPOSE 25 110 143

# The default command to run when the container starts
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
CMD ["postfix", "start-fg"]py