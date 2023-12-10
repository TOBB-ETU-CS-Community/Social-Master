---

<div align="center">

[![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)
[![Poetry](https://img.shields.io/badge/packaging-poetry-cyan.svg)](https://python-poetry.org/)
[![GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

</div>

<hr>

# Social Master

Welcome to the Social Master, a tool designed to automate various social media management tasks on Instagram and Medium. This bot is developed to assist social media managers, influencers, and businesses in efficiently handling their social media accounts.

[WebApp Link](https://insta-bot.streamlit.app/)

## Features

Auto-Liking: Automatically like posts based on hashtags, location, or user feeds to boost engagement and visibility.

Auto-Following: Follow users based on interests, followers, or interactions to grow your audience.

Auto-Unfollowing: Unfollow users who haven't followed you back or based on certain criteria.

Auto-Commenting: Engage with users by leaving comments on their posts using customizable templates.


## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)


## Prerequisites

Before setting up the project, ensure that you have the following prerequisites installed on your machine:

- Python (version 3.10.10):
(https://www.python.org/downloads/)
- Poetry (version 1.4.0):
(https://python-poetry.org/docs/#installation)


## Installation

1. Clone the project repository:

```
git clone https://github.com/TOBB-ETU-CS-Community/Social-Master.git
```

2. Navigate to the project directory:

```
cd social_master
```

3. Install project dependencies using Poetry:

```
poetry install
```

This command will create a virtual environment and install all the necessary dependencies specified in the `pyproject.toml` file.


## Usage

1. Activate the virtual environment created by Poetry:

```
poetry shell
```

2. Run the project:

```
streamlit run "social_master/app.py"
```

## Contributing

If you would like to contribute to this project, follow the guidelines below:

1. Fork the repository and clone it locally.

2. Create a new branch for your feature or bug fix:
   ```
   git checkout -b feature/your-feature
   ```

3. Make your changes and commit them with descriptive commit messages.

4. Push your changes to your forked repository:
   ```
   git push origin feature/your-feature
   ```

5. Open a pull request in the original repository, describing your changes in detail.

## License

GPL v3

---

Happy automating and managing your Social Media accounts!
