# Hyperion Discord Bot

![Hyperion Logo](hyperion_oficial_logo.png)

Hyperion is a versatile Discord bot designed to enhance server management and user engagement. It offers features such as welcome messages, ticketing systems, and whitelist management.

## Features

- **Welcome Messages**: Automatically sends personalized welcome messages to new members joining your server.
- **Ticketing System**: Provides a structured way to handle user inquiries and support requests.
- **Whitelist Management**: Manages a whitelist to control access to specific server features or channels.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/T4skor/Hyperion-Discord-Bot.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd Hyperion-Discord-Bot
   ```

3. **Install the required dependencies**:

   Ensure you have Python installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the bot**:

   ```bash
   python main.py
   ```

## Usage

- **Welcome Messages**:
  - Customize the welcome message in `bienvenidas.py`.
  - Ensure the bot has the necessary permissions to send messages in the desired channel.

- **Ticketing System**:
  - Configure ticket settings in `tickets.py`.
  - Users can create tickets by sending a specific command or reaction, as defined in your configuration.

- **Whitelist Management**:
  - Manage the whitelist through commands defined in `whitelist.py`.
  - Ensure the bot has the appropriate permissions to manage roles or channels as needed.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure your code follows the project's coding standards and includes appropriate documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please open an issue in this repository or contact the project maintainers.
