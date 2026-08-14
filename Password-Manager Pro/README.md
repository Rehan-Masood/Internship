# 🔐 Password Manager Pro

A secure, command-line password manager built in Python with strong encryption, session management, and password strength analysis.

## Demo Video
<video src="https://github.com/user-attachments/assets/c248681f-6342-4936-81d4-533a080a57ea" controls width="600"></video>

## ✨ Features

### 🔑 Core Password Management
- **Add New Passwords**: Store website credentials with optional notes
- **Search Passwords**: Find passwords by website name
- **List All Websites**: View all stored website entries
- **Update Entries**: Modify existing password records
- **Delete Entries**: Securely remove password entries

### 🎲 Password Generation
- **Strong Password Generator**: Cryptographically secure random password generation
- **Customizable Length**: Default 16 characters, configurable as needed
- **Character Options**: Mix of uppercase, lowercase, digits, and symbols
- **Strength Validation**: Built-in password strength checker (Weak, Medium, Strong, Very Strong)

### 🛡️ Security Features
- **Master Password Protection**: Single master password secures entire vault
- **Fernet Encryption**: Industry-standard AES-128 encryption via cryptography library
- **PBKDF2 Key Derivation**: 390,000 iterations for strong key generation against brute-force attacks
- **Random Salt**: Unique 16-byte salt per vault
- **One-Way Verifier**: SHA-256 hash-based verification (password never stored)
- **Timing Attack Prevention**: Constant-time comparison for password verification
- **Session Timeout**: Automatic vault locking after 5 minutes of inactivity
- **Login Lockout**: Protection against brute-force attacks with configurable attempt limits
- **Clipboard Support**: Auto-copy passwords to clipboard with security awareness

### 🔍 Security Audit
- **Weak Password Detection**: Identifies passwords that don't meet strength requirements
- **Reused Password Detection**: Warns when same password is used across multiple websites
- **Security Report**: Comprehensive audit of vault security posture

### ⏱️ Session Management
- **Activity Tracking**: Monitors user activity to prevent vault access during idle periods
- **Background Thread Timer**: Runs independently of CLI input/output
- **Automatic Locking**: Safely locks vault without user intervention

## 📋 Requirements

```
Python 3.8+
cryptography
colorama
pyperclip
```

## 🚀 Installation

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd Password-Manager-Pro
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install cryptography colorama pyperclip
   ```

## 📖 Usage

### Starting the Application

```bash
python main.py
```

### First-Time Setup

On first run, you'll be prompted to:
1. Create a master password (minimum 8 characters recommended)
2. Confirm your master password
3. The vault will be initialized and encrypted

### Main Menu Options

```
========================================
        SECURE PASSWORD MANAGER
========================================
1. Add New Password          - Store new website credentials
2. Search Password by Website - Find a specific password
3. List All Saved Websites   - View all stored entries
4. Update an Entry           - Modify existing password record
5. Delete an Entry           - Remove a password entry
6. Generate a Strong Password - Create a new secure password
7. Security Audit            - Check for weak/reused passwords
8. Change Master Password    - Update your master password
0. Lock & Exit               - Secure vault and exit
```

### Example Workflow

```bash
# 1. Start the application
python main.py

# 2. Unlock vault with master password
Enter master password: ****

# 3. Add a new password
Menu option: 1
Website: github.com
Username: myemail@example.com
Password: (enter or generate)
Notes: My GitHub account

# 4. Search for password
Menu option: 2
Website to search: github.com

# 5. Run security audit
Menu option: 7
(View report of weak/reused passwords)

# 6. Exit securely
Menu option: 0
```

## 📁 Project Structure

```
Password-Manager-Pro/
├── main.py                    # Entry point & CLI interface
├── vault.py                   # Core vault logic & encryption handling
├── password_entry.py          # Password entry data model
├── password_generator.py      # Password generation & strength checking
├── security.py                # Cryptographic utilities & key derivation
├── session_manager.py         # Session timeout & activity tracking
├── vault_data.json           # Encrypted vault storage (auto-created)
└── README.md                  # This file
```

## 🔐 Security Implementation Details

### Encryption Pipeline
1. **Master Password** → PBKDF2 Key Derivation (390,000 iterations) → Fernet Key
2. **Passwords Stored** → Fernet Encryption (AES-128) → JSON Storage
3. **Master Password Verified** → SHA-256 Verifier (one-way hash)

### Key Security Decisions
- Uses `secrets` module (cryptographically secure) instead of `random`
- All sensitive data stored encrypted on disk
- Master password never stored or logged
- Verifier salt prevents rainbow table attacks
- Timing-safe comparison prevents information leakage
- Background session timer ensures vault isn't left unlocked unattended

### Data Storage
- **vault_data.json** contains:
  - Encrypted password entries
  - Salt for key derivation
  - Verifier hash (NOT the password)
- Local file storage only - no cloud or external services

## 🛡️ Best Practices

1. **Master Password**: Use a strong, unique master password (12+ characters, mix of types)
2. **Backups**: Regularly backup `vault_data.json` in a secure location
3. **Physical Security**: Protect your computer from unauthorized access
4. **Session Timeout**: Vault auto-locks after 5 minutes - don't share your computer
5. **Password Generation**: Use the built-in generator for maximum security
6. **Regular Audits**: Run security audits regularly to find weak/reused passwords

## ⚠️ Important Notes

- **No Cloud Backup**: This is a local-only password manager
- **Lost Master Password**: Cannot be recovered - store it securely
- **Database Corruption**: Keep backups of `vault_data.json`
- **Single Master Password**: All security depends on master password strength
- **Not For Production**: Suitable for personal use; evaluate security needs for enterprise use

## 🔧 Development Notes

### Adding New Features
- Extend `Vault` class for core functionality
- Add CLI options in `main.py`
- Use `security.py` utilities for any crypto operations
- Test thoroughly with sample passwords

### Testing Security
- Test with weak/strong/reused passwords
- Verify master password lockout after 5 attempts
- Check session timeout functionality
- Confirm data persists across sessions

## 📝 License

This project is provided as-is for educational purposes.

## 👨‍💻 Contributing

Suggestions for improvements:
- Multi-user support with separate vaults
- Master password change history
- Export/Import encrypted backups
- Two-factor authentication for master password
- Password strength recommendations
- Categories/tags for passwords
- Search with partial matching

## ❓ Troubleshooting

### "Vault locked after too many failed attempts"
- Wait before retrying (limit is 5 attempts)
- Ensure master password is entered correctly

### "Session timeout - vault locked"
- This is a security feature. Re-unlock with your master password
- Adjust `TIMEOUT_SECONDS` in `session_manager.py` if needed (default: 300 seconds)

### "Clipboard error"
- Ensure `pyperclip` is properly installed
- Some Linux systems may need additional setup for clipboard support

### "Encryption/Decryption error"
- Vault file may be corrupted; restore from backup
- Ensure vault file wasn't modified externally

---

**Remember**: Your password security is only as strong as your master password! 🔒
