# Gitlab-Mattermost-Integration
The automatic integration bot to send gitlab hook updates to the mattermost channel

![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSzXbrXuuzBqFBbTXd765b9NMgyL0qM0bzZ2Q&s) | ![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRo68_Lj0l6RoGXpg8fQOJ-O7vP-NQG0WRbQ&s)
--- | ---

# Getting Started
1. Create Incommig hook in mattermost.
2. Update **`appsettings.json`** and replace your data in config file.
3. Update **`users.py`** file in constants folder of src and add your team users. (**Token** is the unique id of user in mattermost)
4. Build and Run the app:
     ```
     sudo docker compose up -d --build
     ```
5. Done!

# Screenshots


# Contributing
Pull requests are welcome. For changes, please open an issue first to discuss what you would like to change.
