# Django SP Admin

[![Django 6.0+](https://img.shields.io/badge/Django-6.0%2B-darkgreen?style=flat-square)](https://www.djangoproject.com/)
[![Python 3.14+](https://img.shields.io/badge/Python-3.14%2B-blue?style=flat-square)](https://www.python.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-4.0+-06B6D4?style=flat-square)](https://tailwindcss.com/)
[![License MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

A sleek, modern Django admin interface override with Tailwind CSS styling, dark mode support, and responsive design. Built on the [Starting Point UI](https://www.startingpointui.com/) design system.

---

## ✨ Features

🎨 **Modern UI** - Clean, responsive design built with Tailwind CSS
🌙 **Dark Mode** - Built-in dark mode toggle
🔍 **Enhanced Admin** - Tabular inlines, filters, search, and more
📱 **Fully Responsive** - Works perfectly on all devices

---

## 📸 Screenshots

TODO: Add some screenshots


## 🚀 Quick Start

This project includes a Dev Container configuration for consistent development environments.

### Prerequisites
- [VS Code](https://code.visualstudio.com/)
- [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [Docker](https://www.docker.com/)

### Getting Started with Dev Container

1. **Open the project in VS Code**
   ```bash
   code .
   ```

2. **Reopen in Container**
   - When prompted, click "Reopen in Container"
   - Or press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) and select "Remote-Containers: Reopen in Container"

3. **Install dependencies and run the development server**
    ```bash
    # Install dependencies
    uv sync

    # load dummy data
    uv load_dummy_data

    # Create superuser
    uv run manage.py createsuperuser

    # Run development server
    uv run manage.py tailwind runserver
    ```

The dev container automatically handles all dependencies and configuration, providing a fully isolated development environment.

Visit [http://localhost:8000/admin](http://localhost:8000/admin) and log in.


## License

MIT License - see [LICENSE](LICENSE) for details.


## Contributing

Contributions welcome! Please submit pull requests or open issues.
