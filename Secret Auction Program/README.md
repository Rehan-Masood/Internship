# Secret Auction Program

A simple command-line Python application that simulates a blind (secret) auction. Bidders can input their names and bids sequentially. The screen clears after each bid, ensuring other participants cannot see previous offers. Once all bids are placed, the program determines and announces the winner with the highest bid.

## 🔨 Features

* **Blind Bidding:** Clears the console screen after each bidder enters their details to maintain confidentiality.
* **Winner Identification:** Analyzes all recorded bids and automatically declares the participant who placed the highest bid.
* **ASCII Art Title:** Features a visual auction gavel logo upon startup.

## 📂 Project Structure

```
Secret Auction Program/
├── Secret_Auction.py   # Main program logic and execution loop
└── art.py              # Contains the ASCII art logo
```

## 🚀 How to Run

### Prerequisites

Ensure you have Python 3 installed on your system.

### Running the Application

1. Open your terminal or command prompt.
2. Navigate to the project directory:
   ```bash
   cd "d:/Future/Internship/Projects/Secret Auction Program"
   ```
3. Run the program using:
   ```bash
   python Secret_Auction.py
   ```

## 📝 Usage Example

1. The game starts and displays the gavel logo.
2. Enter your name and bid amount:
   ```text
   What is your name?: Alice
   What is your bid?: $150
   Are there any other bidders? Type 'yes' or 'no'.
   yes
   ```
3. The screen will clear, allowing the next bidder to enter their bid without seeing the previous bid.
4. Once the final bidder enters their details, type `no` when prompted if there are other bidders.
5. The winner is announced:
   ```text
   The winner is Alice with a bid of $150
   ```
