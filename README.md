# 🔗LinkLiberate🪽

<div>
<p>
  LinkLiberate is a URL shortener that is free and open source. It is built with Python, powered by FastAPI.
</p>
<a href="https://kuma.fosscu.org/status/pastepy" target="_blank"><img src="https://badgen.net/badge/status/LinkLiberate/red?icon=lgtm" alt=""></a>

  ![Version](https://img.shields.io/badge/Version-1.0-brightgreen.svg)
  ![Code Coverage](https://img.shields.io/codecov/c/github/FOSS-Community/LinkLiberate)
  ![License](https://img.shields.io/badge/License-MIT-blue.svg)
  ![GitHub Issues](https://img.shields.io/github/issues/FOSS-Community/LinkLiberate)
  ![GitHub Pull Requests](https://img.shields.io/github/issues-pr/FOSS-Community/LinkLiberate)
  ![Release Date](https://img.shields.io/github/release-date/FOSS-Community/LinkLiberate)
  ![Commits](https://img.shields.io/github/commit-activity/m/FOSS-Community/LinkLiberate)
  ![Last Commit](https://img.shields.io/github/last-commit/FOSS-Community/LinkLiberate)
  ![Contributors](https://img.shields.io/github/contributors/FOSS-Community/LinkLiberate)
  ![Repo Size](https://img.shields.io/github/repo-size/FOSS-Community/LinkLiberate)
  ![Code Size](https://img.shields.io/github/languages/code-size/FOSS-Community/LinkLiberate)

</div>

<p align="center">
  <img width="320" height="320" src="artwork/logo.png" alt="Material Bread logo" style="margin-right:20px;">
</p>


<hr>

# 🤔 Pre-requisites

- `python3`
- `pdm`

## 🐍 Python Version Support

This project is designed to be compatible with specific versions of Python for optimal performance and stability.

### Supported Python Version

- **Python 3.11.6**

> ❗️ For the best experience and performance, it is recommended to use the version mentioned above.

Before diving into the project, ensure that you have the correct Python version installed. To check the version of Python you currently have, execute the following command in your terminal:

```bash
python --version
```

### 🐍 Installing Python 3.11.3 with `pyenv`

**Protip:** Managing multiple Python versions is a breeze with [pyenv](https://github.com/pyenv/pyenv). It allows you to seamlessly switch between different Python versions without the need to reinstall them.

If you haven't installed `pyenv` yet, follow their [official guide](https://github.com/pyenv/pyenv) to set it up.

Once you have `pyenv` ready, install the recommended Python version by running:

```bash
pyenv install 3.11.6
```

> When you navigate to this project's directory in the future, `pyenv` will automatically select the recommended Python version, thanks to the `.python-version` file in the project root.

# 📦 Setup

## Local setup 🛠️ with Docker 🐳

<!--
- **Installing and running**:
  Before you begin, ensure you have docker installed. If not, refer to the [official documentation](https://docs.docker.com/engine/install/) to install docker.
  ```bash
  docker pull mrsunglasses/pastepy
  docker run -d -p 8080:8080 --name pastepyprod mrsunglasses/pastepy
  ```
  -->

- **Using docker-compose**:
  You can also use docker-compose to run the project locally by running the following command:
  <br>
  - **Clone the repository**:
  Get the project source code from GitHub:

  ```bash
  git clone https://github.com/FOSS-Community/LinkLiberate.git
  ```

  - **Navigate to the Project Directory**:

  ```bash
  cd LinkLiberate
  ```

  - **Run the project using docker-compose**:

  ```bash
  docker-compose up
  ```

## Local setup 🛠️ without Docker 🐳

### Setting Up the Project with PDM

[PDM (Python Development Master)](https://pdm.fming.dev/latest/) is utilized for dependency management in this project. To set up and run the project:

- **Installing PDM**:
  Before you begin, ensure you have PDM installed. If not, refer to the [official documentation](https://pdm.fming.dev/latest/) to install PDM.

- **Clone the Repository**:
  Get the project source code from GitHub:

  ```bash
  git clone https://github.com/FOSS-Community/LinkLiberate.git
  ```

- **Navigate to the Project Directory**:

  ```bash
  cd LinkLiberate
  ```

- **Install Dependencies**:
  Use PDM to install the project's dependencies:
  ```bash
  pdm install
  ```

* **Start the Project**:
  Use PDM to run the project:
  ```bash
  pdm run start
  ```

## Setting Up and Testing the Project

To ensure the code quality and functionality of the project, follow the steps below:

### Installing Git Hooks with `pre-commit`

Before making any commits, it's essential to ensure that your code meets the quality standards. This project utilizes `pre-commit` hooks to automatically check your changes before any commit.

Install the pre-commit hooks with the following command:

```bash
pre-commit install
```

### Running Tests

To ensure the project's functionality, you should run all the provided tests. Execute the following command to run the tests:

```bash
pdm run test
```

<!--
### Testing the Running Server

Once you have your server up and running, you can send requests to it from another terminal to test its responsiveness and functionality.

Here are a couple of `GET` requests you can make using [curl](https://curl.se/):

```bash
curl http://0.0.0.0:8080/health
```
-->
> These endpoints typically return the health status or readiness of the server, helping in diagnostics and monitoring.

# 🗒️ How to contribute

> ❗️Important: **Please read the [Code of Conduct](CODE_OF_CONDUCT.md) and go through [Contributing Guideline](CONTRIBUTING.md) before contributing to paste.py**

- Feel free to open an issue for any clarifications or suggestions.

<hr>

<!--
## Uasge:

### Uisng CLI

> cURL is required to use the CLI.

- Paste a file named 'file.txt'

```bash
curl -X POST -F "file=@file.txt" https://paste.fosscu.org/file
```

- Paste from stdin

```bash
echo "Hello, world." | curl -X POST -F "file=@-" https://paste.fosscu.org/file
```

- Delete an existing paste

```bash
curl -X DELETE https://paste.fosscu.org/paste/<id>
```

### Using the web interface:

[Go here](https://paste.fosscu.org/web)

<hr>

For info API usage and shell functions, see the [website](https://paste.fosscu.org).
-->
