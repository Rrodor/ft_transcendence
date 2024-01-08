# FT_TRANSCENDENCE Project

## Overview

FT_TRANSCENDENCE is a project from 42 School that involves creating a comprehensive website with a range of functionalities. This project is an embodiment of versatility and skill in web development, integrating various technologies and tools to build a robust and feature-rich web application.

## Features

The FT_TRANSCENDENCE project includes but is not limited to:

- User authentication and profile management.
- Interactive features such as friends, profile and dashboard, or gaming functionalities.
- Responsive design ensuring compatibility across various devices and screen sizes.
- Advanced backend logic to handle complex web processes.

## Technical Stack

This project utilizes a modern tech stack, ensuring high performance and scalability. Key technologies include:

- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Docker**: A platform for developing, shipping, and running applications inside isolated containers.
- **Nginx**: A high-performance HTTP and reverse proxy server, providing load balancing, caching, and more.
- **PostgreSQL**: An advanced open-source relational database.
- **Bootstrap**: A front-end framework for developing responsive and mobile-first websites.

## Running the Project

To manage the deployment and running of the FT_TRANSCENDENCE project, a custom bash script `transcendence.sh` is used. This script simplifies the process of starting, stopping, and managing the application both in a development (`dev`) and production (`prod`) environment.

### Script Usage

1. **Starting the Server**:
   - In Development Mode: `./transcendence.sh dev start`
   - In Production Mode: `./transcendence.sh prod start`

2. **Running in Background**:
   - Add `bg` at the end of the start command: `./transcendence.sh dev start bg`

3. **Stopping the Server**:
   - `./transcendence.sh dev stop` or `./transcendence.sh prod stop`

4. **Viewing Logs**:
   - Only when running in background mode: `./transcendence.sh dev log bg` or `./transcendence.sh prod log bg`

5. **Checking the Status**:
   - `./transcendence.sh dev status` or `./transcendence.sh prod status`

6. **Cleaning Docker Images and Containers**:
   - `./transcendence.sh clean`

7. **Help**:
   - To view the script usage: `./transcendence.sh help`

### Prerequisites

Before running the script, ensure that Docker and Docker Compose are installed on your system. Also, the script requires `sudo` rights to execute Docker commands.

### Note

Please run the script in the root directory of the project. Ensure the script has execution permissions:

```bash
chmod +x transcendence.sh
```

## License

The FT_TRANSCENDENCE project is open source and is available under the [MIT License](LICENSE.txt).

---
*FT_TRANSCENDENCE - A 42 School Project*
