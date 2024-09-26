# Tauri + React + TypeScript + FastAPI + Vite Template
<img width="912" alt="image" src="https://github.com/user-attachments/assets/4ae49bca-43d2-40c0-ab6e-9d8dcf453fb1">

This template provides a starting point for developing desktop applications using Tauri with a React frontend and a FastAPI backend.

## Features

- **Tauri**: For building lightweight, secure desktop applications
- **React**: For building user interfaces
- **TypeScript**: For adding static type definitions to JavaScript
- **FastAPI**: For creating fast (high-performance) APIs with Python
- **Vite**: For fast frontend tooling

## Project Structure

```
.
├── src/                  # React frontend source files
├── src-python/           # Python FastAPI backend source files
├── src-tauri/            # Tauri configuration and Rust source files
├── public/               # Public assets
├── .gitignore
├── index.html
├── package.json
├── pyproject.toml
├── README.md
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

## Prerequisites

Before you begin, ensure you have the following installed:

- [Node.js](https://nodejs.org/) (v14 or later)
- [Rust](https://www.rust-lang.org/)
- [Python](https://www.python.org/) (v3.12 or later)
- [Poetry](https://python-poetry.org/)
- [npm](https://npmjs.com)

## Getting Started

1. Clone this repository:

   ```
   git clone https://github.com/guilhermeprokisch/tauri-fastapi-react-app.git
   cd tauri-fastapi-react-app
   ```

2. Install frontend dependencies:

   ```
   npm install
   ```

3. Install Python dependencies:

   ```
   poetry install
   ```

4. Run the development server:
   ```
   npm run tauri dev
   ```

This will start both the Tauri/React frontend and the FastAPI backend.

## Project Configuration

- **Frontend**: The React frontend is configured in `vite.config.ts` and `tsconfig.json`.
- **Backend**: The FastAPI backend is configured in `pyproject.toml` and `src-python/main.py`.
- **Tauri**: Tauri configuration is in `src-tauri/tauri.conf.json`.

## Features

- **Integrated Backend**: The FastAPI backend is compiled to a binary and runs as a sidecar process with Tauri.
- **Cross-Platform**: This template supports building for Windows, macOS, and Linux.
- **Hot Reloading**: Enjoy hot reloading for both frontend and backend during development.
- **TypeScript Support**: Full TypeScript support for type-safe code.

## FastAPI Integration

The FastAPI backend is integrated into the Tauri application using the following process:

1. **PyInstaller Compilation**: The FastAPI app is compiled into a standalone executable using PyInstaller. This process is managed by `src-python/pyinstaller.py`.

2. **Sidecar Integration**: The compiled API is registered as an external binary in Tauri's configuration (`src-tauri/tauri.conf.json`) and launched as a sidecar process by the Rust code in `src-tauri/src/main.rs`.

This approach allows for a self-contained application that includes both the frontend and backend, simplifying distribution and deployment.

## TODO and Future Improvements

Here are some planned enhancements for this template:

1. Add an option to skip FastAPI compilation

   - This will allow for faster development cycles when working primarily on the frontend.

2. Implement cross-compilation options

   - Enable building for multiple target platforms from a single development environment.

3. Improve API logging
   - Enhance the logging system for better debugging and monitoring of the FastAPI backend.

Contributions to these improvements are welcome!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
